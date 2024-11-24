from pydantic import BaseModel

class CVEBase(BaseModel):
    cve_id: str
    base_score: float | None = None
    description: str | None = None
    references: list | None = None
