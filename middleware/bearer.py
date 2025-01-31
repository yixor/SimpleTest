from typing import Annotated
from fastapi import Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


def require_auth_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Check if 'Authorization : Bearer {TOKEN}' exists
    """
    return (
        Response(status_code=status.HTTP_401_UNAUTHORIZED)
        if credentials is None
        else credentials.credentials
    )
