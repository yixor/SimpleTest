import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DATABASE
    db_username: str
    db_password: str
    db_address: str
    db_port: str
    db_name: str
    db_default_reciepts_per_page: int = 8
    # PASSWORD UTILS
    salt_rounds: int = 12
    # JWT
    jwt_expires_delta: int = 15  # Minutes
    jwt_secret_key: str  # example: openssl rand -hex 32
    jwt_algorithm: str = "HS256"
    model_config = SettingsConfigDict(env_file=os.getenv("APP_ENV_FILENAME", ".env"))
    # MISC
    app_name: str = "TestAPI"


SETTINGS = Settings()
