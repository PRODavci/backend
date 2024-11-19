import os
from dataclasses import dataclass, asdict
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    # base
    PROJECT_NAME: str = "API"
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    SECRET_KEY: str = os.getenv("APP_SECRET")
    # database
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: int = int(os.getenv("POSTGRES_PORT"))
    DB_NAME: str = os.getenv("POSTGRES_DB")

    DATABASE_URI: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # DATABASE_URI: str = f"sqlite+aiosqlite:///{PROJECT_ROOT}/db.db"
    TEST_DATABASE_URI: str = f"sqlite+aiosqlite:///{PROJECT_ROOT}/test_db.db"

    # auth
    JWT_SECRET: str = os.getenv("APP_SECRET")
    JWT_ACCESS_EXPIRE: timedelta = timedelta(minutes=60)
    JWT_REFRESH_EXPIRE: timedelta = timedelta(days=180)

    def as_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class ProdConfig(Config):
    COOKIE_DOMAIN: str = ""
    CORS_ORIGINS: tuple[str] = ("",)
    SHOW_DOCS: bool = False


@dataclass(frozen=True)
class DevConfig(Config):
    COOKIE_DOMAIN: str = "localhost"
    CORS_ORIGINS: tuple[str] = (
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://localhost",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    )
    SHOW_DOCS: bool = True


def get_config():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevConfig(),
        "prod": ProdConfig(),
    }
    return config_type[env]


config = get_config()
