import enum
from typing import Literal, Optional
from annotated_types import T

from pydantic import BaseModel

from config import SETTINGS


class Product(BaseModel):
    name: str
    price: float
    quantity: int


class PaymentType(enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Payment(BaseModel):
    type: Literal[PaymentType.CASH, PaymentType.CASHLESS]
    amount: float


class RecieptData(BaseModel):
    id: Optional[int] = None
    products: list[Product]
    payment: Payment
    total_amount: Optional[float] = None
    rest: Optional[float] = None


class QueryPair(BaseModel):
    gt: Optional[T]
    ls: Optional[T]


class RecieptsFilter(BaseModel):
    created: Optional[QueryPair]
    total_amount: Optional[QueryPair]
    offset: int = 0
    limit: int = SETTINGS.db_default_reciepts_per_page
