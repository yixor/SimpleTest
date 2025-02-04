from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Double
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from models.reciepts import RecieptData, PaymentType
from orm.database import Base


class Reciept(Base):
    __tablename__ = "reciepts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    total_amount: Mapped[float] = mapped_column(Double, nullable=False)
    type: Mapped[PaymentType] = mapped_column(
        Enum(PaymentType, name="payment_type"), nullable=False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Check(id={self.id}, user_id={self.user_id}, created={self.created})>"

    def to_pydantic_model(self):
        return RecieptData(
            id=self.id,
            products=self.data["products"],
            payment=self.data["payment"],
            rest=self.data["rest"],
            total=self.total_amount,
        )
