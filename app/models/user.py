import datetime as dt

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from utils.time import get_utc


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
    password_updated_at: Mapped[dt.datetime] = mapped_column(default=get_utc)
