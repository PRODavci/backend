from models import PushToken
from repositories.base import SQLAlchemyRepository


class PushTokenRepository(SQLAlchemyRepository):
    model = PushToken
