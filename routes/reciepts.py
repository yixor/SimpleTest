from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.future import select
from sqlalchemy import text

from utils.filters_query import Filter
from middleware.bearer import require_auth_token
from models.reciept import Reciept
from database import SessionDep
from schemas.reciepts import CreateReciept, GetReciept, RecieptsFilter


router = APIRouter(prefix="/reciept", tags=["reciept"])


@router.post("")
async def create_reciept(
    user_id: Annotated[int, Depends(require_auth_token, use_cache=False)],
    cr: CreateReciept,
    db: SessionDep,
):
    total = 0.0
    for product in cr.products:
        product.total = product.quantity * product.price
        total += product.total
    rest = total - cr.payment.amount
    async with db:
        try:
            reciept = Reciept(
                user_id=user_id,
                data=cr.model_dump(),
                total=total,
                rest=rest,
                type=cr.payment.type,
            )
            db.add(reciept)
            await db.commit()
            await db.refresh(reciept)
        except Exception as e:
            await db.rollback()
            raise e

    return reciept.to_pydantic_model()


@router.get("/list")
async def list_personal_reciepts(
    user_id: Annotated[int, Depends(require_auth_token)],
    rf: RecieptsFilter,
    db: SessionDep,
):
    sql_query = Filter.make_query(rf)
    async with db:
        result = await db.execute(
            text(
                f"SELECT * FROM {Reciept.__tablename__} WHERE user_id = {user_id} AND {sql_query}"
            )
        )
    rows = result.fetchall()
    return [
        GetReciept(
            id=row.id,
            data=row.data,
            total=row.total,
            rest=row.rest,
            created=row.created,
        )
        for row in rows
    ]


@router.get("/{reciept_id}")
async def get_reciept(
    reciept_id: int,
    db: SessionDep,
):
    async with db:
        result = await db.execute(select(Reciept).where(Reciept.id == reciept_id))
        reciept = result.scalar_one_or_none()
    if not reciept:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Cannot find reciept by id"
        )
    return reciept.to_pydantic_model()
