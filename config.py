from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GENERAL
    app_name: str = "Test API"
    admin_email: str = "cxndxry@gmail.com"
    # DATABASE
    db_username: str
    db_password: str
    db_address: str
    db_port: str
    db_name: str
    # PASSWORD UTILS
    salt_rounds: int
    # JWT
    jwt_expires_delta: int = 15  # In minutes
    jwt_secret_key: str  # example: openssl rand -hex 32
    jwt_algorithm: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")


SETTINGS = Settings()
