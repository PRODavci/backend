from datetime import datetime

from pydantic import BaseModel

from schemas.host import HostResponse, HostWithoutServicesResponse


class ScanRequest(BaseModel):
    network: str

class ScanResultResponse(BaseModel):
    id: int
    network: str
    timestamp: datetime
    hosts: list[HostResponse]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ScanResultWithoutServicesResponse(BaseModel):
    id: int
    network: str
    timestamp: datetime
    hosts: list[HostWithoutServicesResponse]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ScanResultListResponse(BaseModel):
    data: list[ScanResultWithoutServicesResponse]
