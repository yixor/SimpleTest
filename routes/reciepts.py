from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.future import select
from sqlalchemy import text

from models.users import User
from utils.filters_query import Filter
from middleware.bearer import require_auth_token
from models.reciept import Reciept
from database import SessionDep
from schemas.reciepts import (
    RecieptCreate,
    RecieptGet,
    RecieptGetList,
    RecieptsFilter,
    Payment,
)
from utils.reciept_generator import TextReciept


router = APIRouter(prefix="/reciept", tags=["reciept"])


@router.post(
    "",
    response_model=RecieptGet,
    responses={
        200: {
            "id": 123,
            "products": [
                {
                    "name": "Mavik",
                    "price": 100.0,
                    "quantity": 1,
                    "total": 100.0,
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 100.0,
            },
            "total": 100.0,
            "rest": 0.0,
            "created_at": "2025-12-15T13:24:13",
        },
    },
)
async def create_reciept(
    user_id: Annotated[int, Depends(require_auth_token, use_cache=False)],
    rc: RecieptCreate,
    db: SessionDep,
):
    total = 0.0
    for product in rc.products:
        product.total = product.quantity * product.price
        total += product.total
    rest = total - rc.payment.amount
    with db:
        try:
            reciept = Reciept(
                user_id=user_id,
                products={
                    "products": [product.model_dump() for product in rc.products]
                },
                total=total,
                rest=rest,
                type=rc.payment.type,
            )
            db.add(reciept)
            db.commit()
            db.refresh(reciept)
        except Exception as e:
            db.rollback()
            raise e

    return reciept.to_pydantic_model()


@router.post("/list", response_model=RecieptGetList)
async def list_personal_reciepts(
    user_id: Annotated[int, Depends(require_auth_token)],
    rf: RecieptsFilter,
    db: SessionDep,
):
    sql_query = Filter.make_query(rf)
    with db:
        result = db.execute(
            text(
                f"SELECT * FROM {Reciept.__tablename__} "
                f"WHERE user_id = {user_id} {sql_query}"
            )
        )
    rows = result.fetchall()
    return RecieptGetList(
        reciepts=[
            RecieptGet(
                products=row.products["products"],
                payment=Payment(type=row.type, amount=row.total - row.rest),
                id=row.id,
                total=row.total,
                rest=row.rest,
                created=row.created,
            )
            for row in rows
        ]
    )


@router.get(
    "/{reciept_id}",
    response_model=RecieptGet,
    responses={
        200: {
            "id": 123,
            "products": [
                {
                    "name": "Mavik",
                    "price": 100.0,
                    "quantity": 1,
                    "total": 100.0,
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 100.0,
            },
            "total": 100.0,
            "rest": 0.0,
            "created_at": "2025-12-15T13:24:13",
        },
        404: {
            "description": "Cannot find reciept by id",
            "content": {"text/plain": {"example": "Cannot find reciept by id"}},
        },
    },
)
async def get_reciept(
    reciept_id: int,
    db: SessionDep,
):
    with db:
        result = db.execute(select(Reciept).where(Reciept.id == reciept_id))
        reciept = result.scalar_one_or_none()
    if not reciept:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Cannot find reciept by id"
        )
    return reciept.to_pydantic_model()


@router.get(
    "/{reciept_id}/print",
    responses={
        200: {
            "description": "Plain text response",
            "content": {
                "text/plain": {
                    "example": """
      ФОП Джонсонюк Борис       
================================
3.00 x 298 870.00
Mavic 3T              896 610.00
--------------------------------
20.00 х 31 000.00
Дрон FPV з акумулятором
6S чорний             620 000.00
================================
СУМА                1 516 610.00
Картка              1 516 610.00
Решта                       0.00
================================
        14.08.2023 14:42        
      Дякуємо за покупку!  
                                  
"""
                }
            },
        },
    },
)
async def get_text_reciept(
    reciept_id: int,
    db: SessionDep,
    width: int = 32,
    chapter_char: str = "=",
    product_char: str = "-",
):
    with db:
        result = db.execute(select(Reciept).where(Reciept.id == reciept_id))
        reciept = result.scalar_one_or_none()
        if not reciept:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Cannot find reciept by id",
            )
        user = db.execute(
            select(User).where(User.id == reciept.user_id)
        ).scalar_one_or_none()
        user_name = user.name if user else "DELETED"
    return PlainTextResponse(
        content=TextReciept(
            reciept_width=width,
            reciept=reciept.to_pydantic_model(),
            chapter_char=chapter_char,
            product_char=product_char,
        ).generate_reciept(user_name)
    )
