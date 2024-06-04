import core.exceptions as _exc
from core.security import get_password_hash, verify_password
from models import User
from services.jwt import JWTService
from utils.time import get_utc
from utils.unitofwork import IUnitOfWork
from schemas.user import (
    UserLoginResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse, UserChangePasswordRequest,
)
from schemas.token import TokensResponse


class UserService:
    @staticmethod
    async def _check_email(uow: IUnitOfWork, email: str) -> None:
        if (await uow.user.get(email=email)) is not None:
            raise _exc.ConflictError(detail='User with this email already exists.')

    @staticmethod
    async def get(uow: IUnitOfWork, **filters) -> User | None:
        async with uow:
            user = await uow.user.get(**filters)

            await uow.commit()

            return user

    async def create(self, uow: IUnitOfWork, schema: UserRegisterRequest) -> UserLoginResponse:
        async with uow:
            await self._check_email(uow, schema.email)
            schema.password = get_password_hash(schema.password)

            user = await uow.user.create(schema.model_dump())

            access_token = JWTService().create_token(user.id)
            refresh_token = JWTService().create_token(user.id, refresh=True)

            tokens_schema = TokensResponse(access_token=access_token, refresh_token=refresh_token)
            user_schema = UserResponse.model_validate(user, from_attributes=True)

            await uow.commit()

            return UserLoginResponse(user=user_schema, tokens=tokens_schema)

    @staticmethod
    async def sign_in(uow: IUnitOfWork, schema: UserLoginRequest) -> UserLoginResponse:
        async with uow:
            user = await uow.user.get(email=schema.email)
            if user is not None and verify_password(schema.password, user.password):
                access_token = JWTService().create_token(user.id)
                refresh_token = JWTService().create_token(user.id, refresh=True)

                tokens_schema = TokensResponse(access_token=access_token, refresh_token=refresh_token)
                user_schema = UserResponse.model_validate(user, from_attributes=True)

                await uow.commit()

                return UserLoginResponse(user=user_schema, tokens=tokens_schema)

            raise _exc.AuthError(detail="Invalid login or password.")

    @staticmethod
    async def change_password(uow: IUnitOfWork, user: User, schema: UserChangePasswordRequest):
        async with uow:
            if user is not None and verify_password(schema.old_password, user.password):
                user.password = get_password_hash(schema.new_password)
                user.password_updated_at = get_utc()

                uow.session.add(user)

                await uow.commit()

                return user

            return _exc.ForbiddenError(detail="Invalid current password")
