from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

DATABASE_URL = (
    f'postgresql+asyncpg://{get_settings().postgres_user}:{get_settings().postgres_password}'
    f'@{get_settings().postgres_host}:{get_settings().postgres_port}/{get_settings().postgres_db}'
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    async with async_session() as session:
        yield session
