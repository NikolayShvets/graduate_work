from decimal import Decimal
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload

from api.v1.deps.producer import Producer
from api.v1.deps.session import Session
from api.v1.deps.user import User
from api.v1.deps.yookassa import YooKassa
from api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionRetrieveSchema,
)
from api.v1.schemas.transaction import TransactionCreateSchema
from models import Subscriptions, Tariffs
from models.types import TransactionStatus, TransactionType
from repository.subscription import subscription_repository
from repository.tariff import tariff_repository
from repository.transaction import transaction_repository
from services.producer.schemas import EventType, Notification
from services.producer.schemas import User as ProducerUser
from services.yookassa.dto.amount import Amount
from services.yookassa.dto.confirmation import Confirmation
from services.yookassa.dto.payment import Payment
from services.yookassa.dto.refund import Refund
from services.yookassa.dto.types import ConfirmationType, RefundStatus
from settings.yookassa import settings as yookassa_settings

router = APIRouter()


@router.get("/mine")
async def retrive_mine(session: Session, user: User) -> SubscriptionRetrieveSchema:
    """Получить подписку пользователя."""

    subscription = await subscription_repository.get(session=session, user_id=user.id)

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return subscription


@router.post("")
async def subscribe(
    session: Session,
    yoo_kassa: YooKassa,
    tariff_id: UUID,
    user: User,
) -> SubscriptionRetrieveSchema:
    """Оплатить подписку."""

    if not await tariff_repository.exists(session=session, id=tariff_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if await subscription_repository.exists(session=session, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    tariff: Tariffs = await tariff_repository.get(session=session, id=tariff_id)

    subscription = await subscription_repository.create(
        session=session,
        data=SubscriptionCreateSchema(
            user_id=user.id,
            tariff_id=tariff_id,
        ).model_dump(),
        commit=False,
    )

    payment = await yoo_kassa.create_recurrent_payment(
        amount=Amount(
            value=Decimal(tariff.price) / Decimal(100),
            currency=tariff.currency,
        ),
        confirmation=Confirmation(
            type=ConfirmationType.REDIRECT,
            return_url=yookassa_settings.CONFIRMATION_RETURN_URL,
        ),
        description=tariff.description,
    )

    # TODO: Мб создавать уже в callback?
    await transaction_repository.create(
        session=session,
        data=TransactionCreateSchema(
            payment_id=payment.id,
            subscription_id=subscription.id,
            type=TransactionType.PAYMENT,
        ).model_dump(),
        commit=True,
    )

    return subscription


@router.put("")
async def cancel(
    session: Session, producer: Producer, user: User
) -> SubscriptionRetrieveSchema:
    """Отменить подписку."""

    subscription = await subscription_repository.get(session=session, user_id=user.id)

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await producer.produce(
        Notification(
            id=uuid4(),
            event_type=EventType.SUBSCRIPTION_CANCELED,
            user=ProducerUser(
                email=user.email,
                name=user.email.split("@")[0],
            ),
        )
    )

    return await subscription_repository.update(
        session=session,
        obj=subscription,
        data={"next_payment_date": None},
    )


@router.post("/refund")
async def refund(session: Session, producer: Producer, user: User, yoo_kassa: YooKassa) -> Refund:
    """Вернуть деньги за текущий период подписки."""

    subscription = await subscription_repository.get(
        session=session,
        user_id=user.id,
        options=joinedload(Subscriptions.tariff),
    )

    last_success_payment = await transaction_repository.get_last_success_payment(
        session=session, subscription_id=subscription.id
    )

    if last_success_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    refund = await yoo_kassa.create_refund(
        payment_id=last_success_payment.payment_id,
        amount=Amount(
            value=Decimal(subscription.tariff.price) / Decimal(100),
            currency=subscription.tariff.currency,
        ),
    )

    statuses: dict[RefundStatus, TransactionStatus] = {
        RefundStatus.SUCCEEDED: TransactionStatus.SUCCESS,
        RefundStatus.CANCELED: TransactionStatus.CANCELED,
        RefundStatus.PENDING: TransactionStatus.PENDING,
    }

    await transaction_repository.create(
        session=session,
        data=TransactionCreateSchema(
            payment_id=refund.id,
            subscription_id=subscription.id,
            type=TransactionType.REFUND,
            status=statuses.get(refund.status),
        ).model_dump(),
    )

    await producer.produce(
        Notification(
            id=uuid4(),
            event_type=EventType.SUBSCRIPTION_REFUNDED,
            user=ProducerUser(
                email=user.email,
                name=user.email.split("@")[0],
            ),
        )
    )

    return refund


@router.get("/{user_id}/{movie_id}")
async def movie_is_available(session: Session, user_id: UUID, movie_id: UUID) -> None:
    """Проверить, есть ли переданный фильм в подписке."""

    subscription = await subscription_repository.get_user_active_subscription(
        session=session, user_id=user_id
    )

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    is_available = await subscription_repository.movie_is_available(
        session=session, subscription_id=subscription.id, movie_id=movie_id
    )

    if not is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/payment")
async def get_payment(yoo_kassa: YooKassa, payment_id: UUID) -> Payment:
    """Ручка нужна только для тестов."""
    return await yoo_kassa.get_payment(payment_id=payment_id)
