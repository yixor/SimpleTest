from datetime import datetime, timezone, timedelta

import bcrypt
import jwt
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from config import SETTINGS
from orm.database import Base
from models.tokens import Token


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(48))
    login: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    pass_hash: Mapped[bytes] = mapped_column(LargeBinary(60))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, login={self.login!r}, pass_hash={self.pass_hash!r})"

    def set_password(self, password: str) -> None:
        password_bytes = password.encode("utf-8")
        self.password_hash = bcrypt.hashpw(
            password_bytes, bcrypt.gensalt(SETTINGS.salt_rounds)
        )

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, self.password_hash)

    def create_access_token(self) -> Token:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=SETTINGS.jwt_expires_delta
        )
        to_encode = {"sub": self.id, "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, SETTINGS.jwt_secret_key, algorithm=SETTINGS.jwt_algorithm
        )
        return Token(access_token=encoded_jwt, token_type="Bearer")
