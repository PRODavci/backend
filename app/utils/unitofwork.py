from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_maker
from repositories.cve import CVERepository
from repositories.host import HostRepository
from repositories.scan_result import ScanResultRepository
from repositories.service import ServiceRepository
from repositories.user import UserRepository
from repositories.push_token import PushTokenRepository


class IUnitOfWork(ABC):
    session: AsyncSession
    user: UserRepository
    host: HostRepository
    scan_result: ScanResultRepository
    service: ServiceRepository
    push_token: PushTokenRepository
    cve: CVERepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.host = HostRepository(self.session)
        self.service = ServiceRepository(self.session)
        self.scan_result = ScanResultRepository(self.session)
        self.push_token = PushTokenRepository(self.session)
        self.cve = CVERepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
