from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Double, Enum as SAEnum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from schemas.reciepts import RecieptGet, Product, PaymentType, Payment
from database import Base


class Reciept(Base):
    __tablename__ = "reciepts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    products: Mapped[dict[str, list[dict[str, Any]]]] = mapped_column(
        JSONB, nullable=False
    )
    total: Mapped[float] = mapped_column(Double, nullable=False)
    rest: Mapped[float] = mapped_column(Double, nullable=False)
    type: Mapped[PaymentType] = mapped_column(
        SAEnum(PaymentType, name="payment_type"), nullable=False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Check(id={self.id}, user_id={self.user_id}, created={self.created})>"

    def to_pydantic_model(self):
        return RecieptGet(
            id=self.id,
            payment=Payment(type=self.type, amount=self.total - self.rest),
            products=[Product(**product) for product in self.products["products"]],
            total=self.total,
            rest=self.rest,
            created=self.created,
        )
