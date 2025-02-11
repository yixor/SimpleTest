import logging
from datetime import datetime, timezone
from typing import Annotated, TypeAlias

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import SETTINGS
from schemas.tokens import TokenPayload

security = HTTPBearer()

UserId: TypeAlias = int


def _reject_session():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def require_auth_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserId | Response:
    """
    Check if 'Authorization : Bearer {TOKEN}' exists and verify
    """
    to_return = _reject_session
    if credentials is not None:
        try:
            token_payload = TokenPayload(
                **jwt.decode(
                    credentials.credentials,
                    verify=True,
                    key=SETTINGS.jwt_secret_key,
                    algorithms=[SETTINGS.jwt_algorithm],
                )
            )
            if token_payload.exp > datetime.now(timezone.utc):
                return token_payload.sub
        except jwt.PyJWTError as e:
            logging.warning(f"[{datetime.isoformat()}] Error {e} on JWT decoding")
    return to_return()
