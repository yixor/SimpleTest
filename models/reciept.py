from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Double
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from schemas.reciepts import GetReciept, PaymentType
from database import Base


class Reciept(Base):
    __tablename__ = "reciepts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    products: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    total: Mapped[float] = mapped_column(Double, nullable=False)
    rest: Mapped[float] = mapped_column(Double, nullable=False)
    type: Mapped[PaymentType] = mapped_column(
        Enum(PaymentType, name="payment_type"), nullable=False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Check(id={self.id}, user_id={self.user_id}, created={self.created})>"

    def to_pydantic_model(self):
        return GetReciept(
            id=self.id,
            data=self.data,
            total=self.total,
            rest=self.rest,
            created=self.created,
        )
