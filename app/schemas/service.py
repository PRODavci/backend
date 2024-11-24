from pydantic import BaseModel

from schemas.cve import CVEBase


class ServiceResponse(BaseModel):
    id: int
    host_id: int
    port: int | None = None
    protocol: str | None = None
    name: str | None = None
    product: str | None = None
    version: str | None = None
    ostype: str | None = None
    conf: str | None = None
    cve: list[CVEBase] | None = None
