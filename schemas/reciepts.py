from datetime import datetime
import enum
from typing import Literal, Optional, Any

from pydantic import BaseModel, model_validator

from config import SETTINGS


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    total: Optional[float] = None


class PaymentType(enum.Enum):
    CASH = "CASH"
    CASHLESS = "CASHLESS"


class Payment(BaseModel):
    type: PaymentType
    amount: float


class RecieptCreate(BaseModel):
    products: list[Product]
    payment: Payment
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "products": [
                        {
                            "name": "Mavik",
                            "price": 100000.0,
                            "quantity": 1,
                        },
                    ],
                    "payment": {
                        "type": "cash",
                        "amount": 100000.0,
                    },
                },
            ]
        }
    }


class RecieptGet(RecieptCreate):
    id: int
    total: float
    rest: float
    created: datetime
    model_config = {
        "json_schema_extra": {
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
    }


class RecieptGetList(BaseModel):
    reciepts: list[RecieptGet]


class QueryPair(BaseModel):
    gt: Optional[Any] = None
    eq: Optional[Any] = None
    lw: Optional[Any] = None


class DateTimeQueryPair(QueryPair):
    @model_validator(mode="after")
    def convert_datetime(self):
        if self.gt is not None:
            self.gt = datetime.fromisoformat(self.gt).strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.eq is not None:
            self.eq = datetime.fromisoformat(self.eq).strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.lw is not None:
            self.lw = datetime.fromisoformat(self.lw).strftime("%Y-%m-%d %H:%M:%S.%f")


class RecieptsFilter(BaseModel):
    created: Optional[DateTimeQueryPair] = None
    total: Optional[QueryPair] = None
    type: Optional[PaymentType] = None
    offset: int = 0
    limit: int = SETTINGS.db_default_reciepts_per_page
