import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import Server, Config

from routes import auth


@asynccontextmanager
async def lifespan(_: FastAPI):
    from orm.database import inspect_database

    inspect_database()
    yield


app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(auth.router)


uvicorn = Server(
    Config(
        app=app,
        host="127.0.0.1",
        port=os.getenv("APP_PORT", 8000),
        workers=os.getenv("APP_WORKERS", 4),
    )
)

uvicorn.serve()
