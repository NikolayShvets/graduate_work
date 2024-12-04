from datetime import datetime
from uuid import UUID as PY_UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.types import AutoPaymentPeriod, Currency, TransactionStatus


class Services(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __str__(self):
        return f"Service ({self.id}) {self.name}"


class Services2Movies(Base):
    __table_args__ = (UniqueConstraint("service_id", "movie_id"),)

    service_id: Mapped[PY_UUID] = mapped_column(ForeignKey("services.id"))
    movie_id: Mapped[PY_UUID] = mapped_column(UUID(as_uuid=True))

    def __str__(self):
        return f"Service ({self.id}) has movie {self.movie_id}"


class Plans(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __str__(self):
        return f"Plan ({self.id}) {self.name}"


class Plans2Services(Base):
    __table_args__ = (UniqueConstraint("plan_id", "service_id"),)

    plan_id: Mapped[PY_UUID] = mapped_column(ForeignKey("plans.id"))
    service_id: Mapped[PY_UUID] = mapped_column(ForeignKey("services.id"))

    def __str__(self):
        return f"Plan ({self.id}) has service {self.service_id}"


class Tariffs(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    plan_id: Mapped[PY_UUID] = mapped_column(ForeignKey("plans.id"))
    currency: Mapped[Currency] = mapped_column(ENUM(Currency, name="currency"))
    price: Mapped[int] = mapped_column(Integer)
    auto_payment_period: Mapped[AutoPaymentPeriod] = mapped_column(
        ENUM(AutoPaymentPeriod, name="auto_payment_period")
    )

    subscriptions: Mapped[list["Subscriptions"]] = relationship(
        "Subscriptions", back_populates="tariff"
    )

    def __str__(self):
        return f"Tarrif ({self.id}) {self.name}"

    def get_period_in_days(self) -> int:
        period2days = {
            AutoPaymentPeriod.MONTHLY: 30,
            AutoPaymentPeriod.YEARLY: 365,
        }

        return period2days[self.auto_payment_period]


class Subscriptions(Base):
    user_id: Mapped[PY_UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    tarrif_id: Mapped[PY_UUID] = mapped_column(ForeignKey("tariffs.id"))
    payment_method_id: Mapped[PY_UUID] = mapped_column(UUID(as_uuid=True))
    next_payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=True
    )

    tariff: Mapped[Tariffs] = relationship("Tariffs", back_populates="subscriptions")
    transactions: Mapped[list["Transactions"]] = relationship(
        "Transactions", back_populates="subscription"
    )

    def __str__(self):
        return f"Subscription ({self.id})"

    def is_active(self) -> bool:
        return self.next_payment_date is not None


class Transactions(Base):
    subscription_id: Mapped[PY_UUID] = mapped_column(ForeignKey("subscriptions.id"))
    status: Mapped[TransactionStatus] = mapped_column(
        ENUM(TransactionStatus, name="transaction_status"),
        default=TransactionStatus.PENDING,
    )

    subscription: Mapped[Subscriptions] = relationship(
        "Subscriptions", back_populates="transactions"
    )

    def __str__(self):
        return f"Transaction ({self.id}) {self.status}"
