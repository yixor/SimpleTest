from fastapi import FastAPI
from routes import auth

app = FastAPI(
    debug=True,
)

app.include_router(auth.router)
