from datetime import timedelta

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from api.v1.deps.session import Session
from models import Subscriptions, Transactions
from models.types import TransactionStatus
from repository.subscription import subscription_repository
from repository.transaction import transaction_repository
from services.yookassa.dto.callback import Callback
from services.yookassa.dto.types import EventType

router = APIRouter()


@router.post("/yookassa/callback")
async def callback(session: Session, callback: Callback) -> None:
    transcation = await transaction_repository.get(
        session=session,
        payment_id=callback.object.id,
        options=joinedload(Transactions.subscription).joinedload(Subscriptions.tariff),
    )

    if callback.event == EventType.PAYMENT_SUCCEEDED:
        await transaction_repository.update(
            session=session,
            obj=transcation,
            data={"status": TransactionStatus.SUCCESS},
            commit=False,
        )

        await subscription_repository.update(
            session=session,
            obj=transcation.subscription,
            data={
                "payment_method_id": callback.object.payment_method.id,
                "next_payment_date": (
                    callback.object.created_at
                    + timedelta(
                        days=transcation.subscription.tariff.get_period_in_days()
                    )
                ).replace(tzinfo=None),
            },
            commit=True,
        )

    if callback.event == EventType.PAYMENT_CANCELED:
        await transaction_repository.update(
            session=session,
            obj=transcation,
            data={"status": TransactionStatus.CANCELED},
        )
