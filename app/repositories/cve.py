from models import CVE
from repositories.base import SQLAlchemyRepository


class CVERepository(SQLAlchemyRepository):
    model = CVE
