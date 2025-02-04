from sqlalchemy import MetaData, create_engine
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


def get_async_session() -> AsyncSession:
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


metadata = MetaData()


class Base(DeclarativeBase):
    pass


def inspect_database():
    sync_engine = create_engine(f"postgresql+psycopg2://{connection_url}")
    metadata.reflect(bind=sync_engine)
    metadata.create_all(sync_engine)
