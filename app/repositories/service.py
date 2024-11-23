from models import Service
from repositories.base import SQLAlchemyRepository


class ServiceRepository(SQLAlchemyRepository):
    model = Service
