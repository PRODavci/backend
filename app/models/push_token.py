from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class PushToken(Base):
    __tablename__ = "push_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    token: Mapped[str | None] = mapped_column(String, nullable=True)
