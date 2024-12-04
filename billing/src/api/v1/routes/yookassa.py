from datetime import timedelta

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from api.v1.deps.session import Session
from models import Subscriptions, Transactions
from models.types import TransactionStatus
from repository.subscription import subscription_repository
from repository.transaction import transaction_repository
from services.billing.dto.callback import Callback
from services.billing.dto.types import EventType

router = APIRouter()


@router.post("/yookassa/callback")
async def callback(session: Session, data: Callback) -> None:
    transcation = await transaction_repository.get(
        session=session,
        id=data.object.id,
        options=joinedload(Transactions.subscription).joinedload(Subscriptions.tariff),
    )

    if data.event == EventType.PAYMENT_SUCCEEDED:
        await transaction_repository.update(
            session=session,
            obj=transcation,
            data={"status": TransactionStatus.SUCCESS},
        )

        await subscription_repository.update(
            session=session,
            obj=transcation.subscription,
            data={
                "next_payment_date": data.object.created_at
                + timedelta(days=transcation.subscription.tariff.get_period_in_days())
            },
        )

    if data.event == EventType.PAYMENT_CANCELED:
        await transaction_repository.update(
            session=session,
            obj=transcation,
            data={"status": TransactionStatus.CANCELED},
        )
