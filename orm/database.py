from sqlalchemy.ext.asyncio import create_async_engine

from config import SETTINGS

engine = create_async_engine(
    f"postgresql+asyncpg://"
    f"{SETTINGS.db_user}:{SETTINGS.db_password}"
    f"@{SETTINGS.db_host}:{SETTINGS.db_port}"
    f"/{SETTINGS.db_name}",
    echo=True,
)
