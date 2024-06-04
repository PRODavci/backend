from jose import JWTError, jwt

from core.config import config
from schemas.token import TokensResponse
from utils.time import get_utc_timestamp

JWT_SECRET = config.JWT_SECRET
JWT_ACCESS_EXPIRE = config.JWT_ACCESS_EXPIRE
JWT_REFRESH_EXPIRE = config.JWT_REFRESH_EXPIRE


class JWTService:
    @staticmethod
    def create_token(_id: int, refresh=False) -> str:
        expire = JWT_REFRESH_EXPIRE if refresh else JWT_ACCESS_EXPIRE
        token_type = 'refresh' if refresh else 'access'
        data = {
            'sub': str(_id),
            'type': token_type,
            'exp': get_utc_timestamp() + expire.total_seconds(),
            'iat': get_utc_timestamp()
        }
        encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm="HS256")  # type: ignore
        return encoded_jwt

    @staticmethod
    def get_token_data(token: str) -> dict | None:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms="HS256", )  # type: ignore
            payload['sub'] = int(payload['sub'])
            return payload
        except JWTError as e:
            print(e)
            return None
        except AttributeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

    def refresh(self, refresh_token: str) -> TokensResponse | None:
        if not refresh_token:
            return None

        token_data = self.get_token_data(refresh_token)

        if not token_data or not token_data.get('type') == 'refresh':
            return None

        access_token = self.create_token(token_data['sub'])
        refresh_token = self.create_token(token_data['sub'], refresh=True)

        return TokensResponse(access_token=access_token, refresh_token=refresh_token)

