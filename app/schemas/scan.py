from pydantic import BaseModel


class ScanRequest(BaseModel):
    network: str
