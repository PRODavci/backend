from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.v1.routes import routers as v1_router
from core.config import config


async def on_startup():
    pass


async def on_shutdown():
    pass


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await on_startup()

    yield

    await on_shutdown()


def init_routers(app_: FastAPI):
    app_.include_router(v1_router)


def make_middleware():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=config.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SessionMiddleware, secret_key=config.SECRET_KEY),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="API",
        description="API",
        version="1.0.0",
        docs_url=None if not config.SHOW_DOCS else "/docs",
        redoc_url=None if not config.SHOW_DOCS else "/redoc",
        middleware=make_middleware(),
        lifespan=lifespan,
    )
    init_routers(app_=app_)
    return app_


app = create_app()
