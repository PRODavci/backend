from pydantic import BaseModel

from schemas.service import ServiceResponse


class HostResponse(BaseModel):
    id: int
    ip: str
    services: list[ServiceResponse]

class HostWithoutServicesResponse(BaseModel):
    id: int
    ip: str
