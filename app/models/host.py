from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.service import Service
    from models.scan_result import ScanResult


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)
    services: Mapped[list["Service"]] = relationship(
        back_populates="host", cascade="all, delete-orphan", lazy="selectin",
    )
    scan_result_id: Mapped[int] = mapped_column(ForeignKey("scan_results.id"))
    scan_result: Mapped["ScanResult"] = relationship(back_populates="hosts")
