import asyncio
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from core.config import config
from services.scan import ScanService
from utils.unitofwork import UnitOfWork

RABBIT_HOST = config.RABBITMQ_HOST
RABBIT_PORT = config.RABBITMQ_PORT
RABBITMQ_USER = config.RABBITMQ_USER
RABBITMQ_PASSWORD = config.RABBITMQ_PASSWORD


async def process_alive_hosts(data: dict):
    """
    Обрабатывает данные типа 'alive_hosts': добавляет живые хосты в текущий результат сканирования.
    """
    uow = UnitOfWork()

    scan_result_id = data.get('scan_result_id')
    alive_hosts = data.get('data', [])

    if not scan_result_id or not alive_hosts:
        print("Invalid data for alive_hosts")
        return


    await ScanService().add_alive_hosts(uow, scan_result_id, alive_hosts)
    print(f"Added alive hosts to scan result {scan_result_id}: {alive_hosts}")


async def process_hosts_services(data: dict):
    """
    Обрабатывает данные типа 'host_service': добавляет сервисы для хоста в текущий результат сканирования.
    """
    uow = UnitOfWork()

    scan_result_id = data.get('scan_result_id')
    host_ip = data['data'].get('host')
    services = data['data'].get('services', [])

    if not scan_result_id or not host_ip or not services:
        print("Invalid data for host_service")
        return

    await ScanService().add_services(uow, scan_result_id, host_ip, services)
    print(f"Added services for host {host_ip} in scan result {scan_result_id}")


async def process_scan_finished(data: dict):
    """
    Обрабатывает данные типа 'scan_finished': завершает сканирование и сравнивает с предыдущим результатом.
    """
    uow = UnitOfWork()

    scan_result_id = data.get('scan_result_id')
    network = data.get('network')

    if not scan_result_id or not network:
        print("Invalid data for scan_finished")
        return

    differences = await ScanService().compare_scan_results(uow, scan_result_id, network)
    print(f"Scan result {scan_result_id} finished. Differences with previous scan:")
    for diff in differences:
        print(diff)


async def receive_message():
    print(RABBIT_HOST, RABBIT_PORT)
    print(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('backend-api')

        async def on_message(message: AbstractIncomingMessage) -> None:
            data = message.body.decode()
            data = json.loads(data)
            print(" [x] Received dictionary :", data)

            if data['type'] == 'alive_hosts':
                await process_alive_hosts(data)

            elif data['type'] == 'host_service':
                await process_hosts_services(data)

            elif data['type'] == 'scan_finished':
                await process_scan_finished(data)

            await message.ack()

        await queue.consume(on_message)
        await asyncio.Future()


def start_consumer():
    print(" [x] Start receiving")
    asyncio.run(receive_message())
