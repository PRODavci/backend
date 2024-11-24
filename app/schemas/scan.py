from datetime import datetime

from pydantic import BaseModel

from schemas.cve import CVEBase
from schemas.host import HostResponse, HostWithoutServicesResponse


class ScanRequest(BaseModel):
    network: list[str]

class ScanResultResponse(BaseModel):
    id: int
    network: str
    timestamp: datetime
    status: str
    hosts: list[HostResponse]
    cve: list[CVEBase]


    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ScanResultWithoutServicesResponse(BaseModel):
    id: int
    network: str
    timestamp: datetime
    status: str
    hosts: list[HostWithoutServicesResponse]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ScanResultListResponse(BaseModel):
    data: list[ScanResultWithoutServicesResponse]
