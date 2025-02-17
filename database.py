from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from config import SETTINGS

connection_url = f"{SETTINGS.db_username}:{SETTINGS.db_password}@{SETTINGS.db_address}:{SETTINGS.db_port}/{SETTINGS.db_name}"
engine = create_engine(
    f"postgresql+psycopg2://{connection_url}",
    echo=True,
)

session_maker = sessionmaker(engine, expire_on_commit=False)


def get_db():
    return session_maker()


SessionDep = Annotated[Session, Depends(get_db)]


class Base(DeclarativeBase):
    pass


def init_db_sync():
    Base.metadata.create_all(engine)
