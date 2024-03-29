from functools import lru_cache

from core.config import settings
from db.models import users, vacansies
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.postgres.uri, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(users.Base.metadata.create_all)
        await conn.run_sync(vacansies.Base.metadata.create_all)


@lru_cache()
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
