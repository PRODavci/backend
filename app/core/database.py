from sys import modules
from typing import AsyncGenerator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from core.config import config


engine = create_async_engine(config.DATABASE_URI, echo=False)

if 'pytest' in modules:
    engine = create_async_engine(config.TEST_DATABASE_URI)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
