from models import Host
from repositories.base import SQLAlchemyRepository


class HostRepository(SQLAlchemyRepository):
    model = Host
