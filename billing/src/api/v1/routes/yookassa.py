from datetime import timedelta
from uuid import uuid4

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from api.v1.deps.producer import Producer
from api.v1.deps.session import Session
from clients.auth.client import auth_client
from models import Subscriptions, Transactions
from models.types import TransactionStatus
from repository.subscription import subscription_repository
from repository.transaction import transaction_repository
from services.producer.schemas import EventType as ProducerEventType
from services.producer.schemas import Notification, User
from services.yookassa.dto.callback import Callback
from services.yookassa.dto.types import EventType

router = APIRouter()


@router.post("/yookassa/callback")
async def callback(session: Session, producer: Producer, callback: Callback) -> None:
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

        user = await auth_client.get_user(user_id=transcation.subscription.user_id)

        await producer.produce(
            Notification(
                id=uuid4(),
                event_type=ProducerEventType.SUBSCRIPTION_PAID,
                user=User(
                    email=user.email,
                    name=user.email.split("@")[0],
                ),
            )
        )

    if callback.event == EventType.PAYMENT_CANCELED:
        await transaction_repository.update(
            session=session,
            obj=transcation,
            data={"status": TransactionStatus.CANCELED},
        )
