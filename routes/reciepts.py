from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.future import select
from sqlalchemy import and_, text

from middleware.bearer import require_auth_token
from orm.reciept import Reciept
from orm.database import get_async_session
from models.reciepts import RecieptData, RecieptsFilter


router = APIRouter(prefix="/reciept", tags=["reciept"])


@router.post("")
async def create_reciept(
    user_id: Annotated[int, Depends(require_auth_token, use_cache=False)],
    reciept_data: RecieptData,
):

    reciept_data.total = sum(
        product.quantity * product.price for product in reciept_data.products
    )
    reciept_data.rest = reciept_data.total - reciept_data.payment.amount
    async with get_async_session() as s:
        try:
            reciept = Reciept(
                user_id=user_id,
                data=reciept_data.model_dump(),
                total_amount=reciept_data.total,
                type=reciept_data.payment.type,
            )
            s.add(reciept)
            await s.commit()
            await s.refresh(reciept)
            reciept_data = reciept.id
        except Exception as e:
            await s.rollback()
            raise e
    return reciept_data


@router.get("/list")
async def list_personal_reciepts(
    user_id: Annotated[int, Depends(require_auth_token)],
    filter_query: Annotated[RecieptsFilter, Query()],
):

    async with get_async_session() as s:

        s.execute(text())


@router.get("/{reciept_id}")
async def get_reciept(reciept_id: int):
    async with get_async_session() as s:
        result = await s.execute(select(Reciept).where(Reciept.id == reciept_id))
        reciept = result.scalar_one_or_none()
    if not reciept:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Cannot find reciept by id"
        )

    return reciept.to_pydantic_model()
