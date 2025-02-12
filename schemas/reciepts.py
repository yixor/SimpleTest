from datetime import datetime
import enum
from typing import Literal, Optional, Any

from pydantic import BaseModel

from config import SETTINGS


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    total: Optional[float] = None


class PaymentType(enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Payment(BaseModel):
    type: PaymentType
    amount: float


class RecieptCreate(BaseModel):
    products: list[Product]
    payment: Payment


class RecieptGet(RecieptCreate):
    id: int
    total: float
    rest: float
    created: datetime


class QueryPair(BaseModel):
    gt: Optional[Any] = None
    eq: Optional[Any] = None
    lw: Optional[Any] = None


class RecieptsFilter(BaseModel):
    created: Optional[QueryPair]
    total: Optional[QueryPair]
    type: Optional[PaymentType]
    offset: int = 0
    limit: int = SETTINGS.db_default_reciepts_per_page
