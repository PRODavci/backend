from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from utils.time import get_utc

if TYPE_CHECKING:
    from models.host import Host


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    network: Mapped[str] = mapped_column(String(1000))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=get_utc)
    status: Mapped[str] = mapped_column(String(50), default="running")
    hosts: Mapped[list["Host"]] = relationship(
        "Host", back_populates="scan_result", cascade="all, delete-orphan", lazy="selectin"
    )
