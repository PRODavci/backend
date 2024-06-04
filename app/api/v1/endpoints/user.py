from fastapi import APIRouter, Response

from core.dependencies import UOW, current_user_or_error
from core.config import config
from schemas.user import (
    UserLoginResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    UserChangePasswordRequest
)
from services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('', response_model=UserLoginResponse)
async def register_user(uow: UOW, response: Response, schema: UserRegisterRequest):
    response_schema = await UserService().create(uow, schema)
    response.set_cookie('refresh_token',
                        response_schema.tokens.refresh_token,
                        httponly=True,
                        domain=config.COOKIE_DOMAIN,
                        path='/',
                        expires=config.JWT_REFRESH_EXPIRE,
                        samesite='strict',
                        secure=True,
                        )
    return response_schema


@router.post('/login', response_model=UserLoginResponse)
async def login_user(uow: UOW, response: Response, schema: UserLoginRequest):
    response_schema = await UserService().sign_in(uow, schema)
    response.set_cookie('refresh_token',
                        response_schema.tokens.refresh_token,
                        httponly=True,
                        domain=config.COOKIE_DOMAIN,
                        path='/',
                        expires=config.JWT_REFRESH_EXPIRE,
                        samesite='strict',
                        secure=True,
                        )
    return response_schema


@router.get('/me', response_model=UserResponse)
async def me(current_user: current_user_or_error):
    response_schema = UserResponse.model_validate(current_user, from_attributes=True)
    return response_schema


@router.post('/change_password', response_model=UserResponse)
async def change_user_password(uow: UOW, current_user: current_user_or_error, schema: UserChangePasswordRequest):
    user = await UserService().change_password(uow, current_user, schema)
    response_schema = UserResponse.model_validate(user, from_attributes=True)
    return response_schema
