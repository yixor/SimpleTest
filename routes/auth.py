from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select

from database import SessionDep
from models.users import User
from schemas.tokens import Token
from schemas.users import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    responses={
        404: {
            "description": "Cannot find user by login",
            "content": {
                "text/plain": {"example": "A user with this name could not be found"}
            },
        },
        401: {
            "description": "Incorrect username or password",
            "content": {"text/plain": {"example": "Incorrect username or password"}},
        },
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
) -> Token:
    with db:
        result = db.execute(select(User).where(User.login == form_data.username))
        user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A user with this name could not be found",
        )
    if not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.create_access_token()


@router.post(
    "/signup",
    responses={
        409: {
            "description": "A user with this name already exists",
            "content": {
                "text/plain": {"example": "A user with this name already exists"}
            },
        },
    },
)
async def sign_up(
    user_create: UserCreate,
    db: SessionDep,
):
    with db:
        result = db.execute(select(User).where(User.login == user_create.login))
        exist_user = result.scalar_one_or_none()
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this name already exists",
            )
        user = User(
            name=user_create.name,
            login=user_create.login,
            pass_hash=User.gen_password(user_create.password),
        )
        db.add(user)
        db.commit()

    return Response(status_code=status.HTTP_201_CREATED)
