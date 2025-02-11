from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import SETTINGS

connection_url = (
    f"{SETTINGS.db_username}:{SETTINGS.db_password}"
    f"@{SETTINGS.db_address}:{SETTINGS.db_port}"
    f"/{SETTINGS.db_name}"
)
engine = create_async_engine(
    f"postgresql+asyncpg://{connection_url}",
    echo=True,
)


def get_db() -> AsyncSession:
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


SessionDep = Annotated[AsyncSession, Depends(get_db)]


class Base(DeclarativeBase):
    pass


async def inspect_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())
