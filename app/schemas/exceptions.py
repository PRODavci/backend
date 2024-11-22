from pydantic import BaseModel


class ExceptionErrorResponse(BaseModel):
    detail: str
