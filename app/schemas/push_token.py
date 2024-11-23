from pydantic import BaseModel


class PushTokenRequest(BaseModel):
    token: str
