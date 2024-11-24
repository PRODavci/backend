from sqlalchemy import Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base


class CVE(Base):
    __tablename__ = "cves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)  # Связь с Service
    cve_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # CVE ID
    base_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # Base Score (CVSS)
    description: Mapped[str | None] = mapped_column(String, nullable=True)  # Описание CVE
    references: Mapped[list | None] = mapped_column(JSON, nullable=True)  # Массив ссылок (JSON)

    service: Mapped["Service"] = relationship("Service", back_populates="cves")
