from fastapi import APIRouter, Response, Request, status

from core.config import config
from core.exceptions import AuthError
from schemas.exceptions import ExceptionErrorResponse
from schemas.token import TokensResponse, RefreshTokenRequest
from services.jwt import JWTService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/refresh",
    response_model=TokensResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": TokensResponse,
            "description": "Ok Response",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionErrorResponse,
            "description": "Incorrect refresh token",
        },
    },
)
async def refresh_access(request: Request, response: Response, schema: RefreshTokenRequest = None):
    refresh_token = request.cookies.get("refresh_token", None)

    if schema is not None and schema.refresh_token is not None:
        refresh_token = schema.refresh_token

    response_schema = JWTService().refresh(refresh_token)

    if not response_schema:
        raise AuthError("Invalid refresh token.")

    response.set_cookie(
        "refresh_token",
        response_schema.refresh_token,
        httponly=True,
        domain=config.COOKIE_DOMAIN,
        path="/",
        expires=config.JWT_REFRESH_EXPIRE,
        samesite="strict",
        secure=True,
    )
    return response_schema


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"status": "success"}
