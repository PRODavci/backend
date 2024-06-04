from fastapi import APIRouter, Response, Request

from core.config import config
from core.exceptions import AuthError
from schemas.token import TokensResponse
from services.jwt import JWTService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/refresh", response_model=TokensResponse)
async def refresh_access(request: Request, response: Response):
    token = request.cookies.get('refresh_token')
    response_schema = JWTService().refresh(token)

    if not response_schema:
        raise AuthError('Invalid refresh token.')

    response.set_cookie('refresh_token',
                        response_schema.refresh_token,
                        httponly=True,
                        domain=config.COOKIE_DOMAIN,
                        path='/',
                        expires=config.JWT_REFRESH_EXPIRE,
                        samesite='strict',
                        secure=True,
                        )
    return response_schema


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie('refresh_token')
    return {'status': 'success'}
