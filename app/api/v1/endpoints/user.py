from fastapi import APIRouter, Response, status

from core.config import config
from core.dependencies import UOW, CurrentUserOrError
from schemas.exceptions import ExceptionErrorResponse
from schemas.push_token import PushTokenRequest
from schemas.user import (
    UserLoginResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    UserChangePasswordRequest,
)
from services.push_token import PushTokenService
from services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    response_model=UserLoginResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserLoginResponse,
            "description": "Ok Response",
        },
        status.HTTP_409_CONFLICT: {
            "model": ExceptionErrorResponse,
            "description": "User with this email already exists",
        },
    },
)
async def register_user(uow: UOW, response: Response, schema: UserRegisterRequest):
    response_schema = await UserService().create(uow, schema)
    response.set_cookie(
        "refresh_token",
        response_schema.tokens.refresh_token,
        httponly=True,
        domain=config.COOKIE_DOMAIN,
        path="/",
        expires=config.JWT_REFRESH_EXPIRE,
        samesite="strict",
        secure=True,
    )
    return response_schema


@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={
        status.HTTP_200_OK: {
            "model": UserLoginResponse,
            "description": "Ok Response",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionErrorResponse,
            "description": "Invalid email or password",
        },
    },
)
async def login_user(uow: UOW, response: Response, schema: UserLoginRequest):
    response_schema = await UserService().sign_in(uow, schema)
    response.set_cookie(
        "refresh_token",
        response_schema.tokens.refresh_token,
        httponly=True,
        domain=config.COOKIE_DOMAIN,
        path="/",
        expires=config.JWT_REFRESH_EXPIRE,
        samesite="strict",
        secure=True,
    )
    return response_schema


@router.get(
    "/me", response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
            "description": "Ok Response",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionErrorResponse,
            "description": "Invalid auth token",
        },
    },
)
async def me(current_user: CurrentUserOrError):
    response_schema = UserResponse.model_validate(current_user, from_attributes=True)
    return response_schema


@router.post(
    "/change_password",
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
            "description": "Ok Response",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionErrorResponse,
            "description": "Invalid auth token",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ExceptionErrorResponse,
            "description": "Invalid current password",
        },
    },
)
async def change_user_password(uow: UOW, current_user: CurrentUserOrError, schema: UserChangePasswordRequest):
    user = await UserService().change_password(uow, current_user, schema)
    response_schema = UserResponse.model_validate(user, from_attributes=True)
    return response_schema

@router.post(
    "/push_token",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponse,
            "description": "Ok Response",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionErrorResponse,
            "description": "Invalid auth token",
        },
    },
)
async def add_token(uow:UOW,  current_user: CurrentUserOrError, schema: PushTokenRequest):
    await PushTokenService().create(uow, current_user.id, schema.token)
    return {'status': 'ok'}
