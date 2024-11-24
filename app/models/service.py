from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.host import Host


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    host_id: Mapped[int | None] = mapped_column(ForeignKey("hosts.id"), nullable=True)
    port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    product: Mapped[str | None] = mapped_column(String, nullable=True)
    version: Mapped[str | None] = mapped_column(String, nullable=True)
    ostype: Mapped[str | None] = mapped_column(String, nullable=True)
    conf: Mapped[str | None] = mapped_column(String, nullable=True)

    host: Mapped["Host"] = relationship(back_populates="services")
    cves: Mapped[list["CVE"]] = relationship("CVE", back_populates="service", cascade="all, delete-orphan",
                                             lazy="selectin")
