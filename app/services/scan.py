import aiohttp
from sqlalchemy import select, and_

from core.config import config
from core.exceptions import NotFoundError
from models import ScanResult
from schemas.scan import ScanResultResponse, ScanResultListResponse
from utils.unitofwork import IUnitOfWork


class ScanService:
    @staticmethod
    async def create(uow: IUnitOfWork, network: str):
        async with uow:
            scan_result = await uow.scan_result.create({
                'network': network,
            })

            await uow.commit()

        return scan_result

    @staticmethod
    async def get_list(uow: IUnitOfWork, limit: int = None, offset: int = None, order_by: str = None,
                       reverse: bool = False, **filter_by):
        async with uow:
            scan_results = await uow.scan_result.get_list(limit, offset, order_by, reverse, **filter_by)

            await uow.commit()

            return ScanResultListResponse.model_validate(scan_results, from_attributes=True)

    @staticmethod
    async def get(uow: IUnitOfWork, **filters) -> ScanResultResponse:
        async with uow:
            scan_result = await uow.scan_result.get(**filters)

            if not scan_result:
                raise NotFoundError('Scan result with this id not found')

            await uow.commit()

            return ScanResultResponse.model_validate(scan_result, from_attributes=True)

    @staticmethod
    async def _get_last_scan_result(uow: IUnitOfWork, current_scan_result_id: int, network: str) -> ScanResult | None:
        async with uow:
            last_scan_result = await uow.session.execute(
                select(ScanResult)
                .where(and_(ScanResult.id < current_scan_result_id, ScanResult.network == network))
                .order_by(ScanResult.id.desc())
                .limit(1)
            )
            result = last_scan_result.scalar_one_or_none()
            await uow.commit()

        return result

    @staticmethod
    async def add_alive_hosts(uow: IUnitOfWork, scan_result_id: int, alive_hosts: list[str]):
        async with uow:
            for ip in alive_hosts:
                host = await uow.host.get(ip=ip, scan_result_id=scan_result_id)
                print(host)
                if not host:
                    await uow.host.create({
                        'ip': ip,
                        'scan_result_id': scan_result_id,
                    })
            await uow.commit()


    @staticmethod
    async def add_services(uow: IUnitOfWork, scan_result_id: int, host_ip: str, services: list[dict]):
        async with uow:
            host = await uow.host.get(ip=host_ip, scan_result_id=scan_result_id)
            if not host:
                raise ValueError(f"Host {host_ip} not found in scan result {scan_result_id}.")

            for service_data in services:
                service = await uow.service.get(
                    host_id=host.id,
                    port=int(service_data['port']),
                    protocol=service_data['protocol']
                )
                if not service:
                    service = await uow.service.create({
                        'host_id': host.id,
                        'port': int(service_data['port']),
                        'protocol': service_data['protocol'],
                        'name': service_data['name'],
                        'product': service_data['product'],
                        'version': service_data['version'],
                        'ostype': service_data['ostype'],
                        'conf': service_data['conf'],
                    })

                    await uow.commit()

                    print(service_data)

                    if service_data['product'] is not None and service_data['version'] is not None:
                        cve_list = fetch_cve(service_data['product'], service_data['version'])
                        if cve_list:
                            print(cve_list)
                            for cve in cve_list:

                                await uow.cve.create({
                                    'service_id': service.id,
                                    'cve_id': cve['cve_id'],
                                    'base_score':cve['metrics']['base_score'],
                                    'description':cve['meta']['base_score'],
                                    'references': cve['references'],
                                })

                            await uow.commit()
                else:
                    for key in ['name', 'product', 'version', 'ostype', 'conf']:
                        if getattr(service, key) != service_data.get(key):
                            setattr(service, key, service_data.get(key))
                    uow.session.add(service)

            await uow.commit()

    @staticmethod
    async def compare_scan_results(uow: IUnitOfWork, current_scan_result_id: int, network: str) -> list[str] | None:
        """
        Сравнивает текущий результат сканирования с предыдущим.
        Возвращает список изменений.
        """
        async with uow:
            last_scan_result = await ScanService._get_last_scan_result(uow, current_scan_result_id, network)
            if not last_scan_result:
                return None

            current_hosts = {
                host.ip: host for host in (await uow.host.get_list(scan_result_id=current_scan_result_id))['data']
            }
            previous_hosts = {
                host.ip: host for host in (await uow.host.get_list(scan_result_id=last_scan_result.id))['data']
            }

            differences = []

            for ip, current_host in current_hosts.items():
                if ip not in previous_hosts:
                    differences.append(f"Найден новый хост: {ip}")
                else:
                    current_services = {f"{s.port}/{s.protocol}": s for s in current_host.services}
                    previous_services = {f"{s.port}/{s.protocol}": s for s in previous_hosts[ip].services}

                    for key, current_service in current_services.items():
                        if key not in previous_services:
                            differences.append(f"Найден новый сервис {ip}: {key}")
                        else:
                            previous_service = previous_services[key]
                            for param in ['name', 'product', 'version', 'ostype', 'conf']:
                                if getattr(current_service, param) != getattr(previous_service, param):
                                    differences.append(
                                        f"Сервис {key} на хосте {ip} изменил {param}: "
                                        f"{getattr(previous_service, param)} -> {getattr(current_service, param)}"
                                    )

            for ip in previous_hosts.keys():
                if ip not in current_hosts:
                    differences.append(f"Хост больше не доступен: {ip}")

            return differences

    @staticmethod
    async def update_status(uow: IUnitOfWork, scan_result_id: int, status: str):
        async with uow:
            scan_result = await uow.scan_result.get(id=scan_result_id)
            if not scan_result:
                return None

            scan_result.status = status
            uow.session.add(scan_result)

            await uow.commit()


async def fetch_cve(product: str, version: str) -> list:
    base_url = f"http://{config.CVE_SERVICE_URL}:{config.CVE_SERVICE_PORT}/search"
    params = {
        "product": product,
        "version": version,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к CVE-сервису: {e}")
            return None
