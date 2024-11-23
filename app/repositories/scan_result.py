from models import ScanResult
from repositories.base import SQLAlchemyRepository


class ScanResultRepository(SQLAlchemyRepository):
    model = ScanResult
