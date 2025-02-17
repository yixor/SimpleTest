from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db_sync
from routes import auth, reciepts


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db_sync()
    yield


app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(auth.router)
app.include_router(reciepts.router)
