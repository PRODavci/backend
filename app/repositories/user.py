from models import User
from repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
