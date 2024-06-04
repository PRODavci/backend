from pydantic import BaseModel, EmailStr
from schemas.token import TokensResponse


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserLoginResponse(BaseModel):
    user: UserResponse
    tokens: TokensResponse


class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
