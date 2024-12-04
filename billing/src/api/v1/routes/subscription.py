from decimal import Decimal

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.billing import YooKassa
from api.v1.deps.session import Session
from api.v1.deps.user import User
from api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionRetrieveSchema,
)
from api.v1.schemas.transaction import TransactionCreateSchema
from models import Tariffs
from repository.subscription import subscription_repository
from repository.tariff import tariff_repository
from repository.transaction import transaction_repository
from services.billing.dto.amount import Amount
from services.billing.dto.payment import Payment

router = APIRouter()


@router.get("/subscriptions/mine")
async def retrive_mine(session: Session, user: User) -> SubscriptionRetrieveSchema:
    """Получить подписку пользователя."""

    subscription = await subscription_repository.get(session=session, user_id=user.id)

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return subscription


@router.post("/subscriptions")
async def create(
    session: Session,
    yoo_kassa: YooKassa,
    data: SubscriptionCreateSchema,
    _: User,
) -> SubscriptionRetrieveSchema:
    """Создать подписку."""

    if await subscription_repository.exists(session=session, user_id=data.user_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    tariff: Tariffs = await tariff_repository.get(session=session, id=data.tarrif_id)

    payment: Payment = await yoo_kassa.create_payment(
        amount=Amount(
            value=Decimal(tariff.price) / Decimal(100),
            currency=tariff.currency,
        ),
        auto_payment=True,
    )
    subscription = await subscription_repository.create(
        session=session,
        data=data.model_dump() | {"payment_method_id": payment.payment_method.id},
        commit=False,
    )
    await transaction_repository.create(
        session=session,
        data=TransactionCreateSchema(
            id=payment.id,
            subscription_id=subscription.id,
        ).model_dump(),
        commit=True,
    )

    return subscription


async def cancel(session: Session, user: User) -> SubscriptionRetrieveSchema:
    """Отменить подписку."""

    subscription = await subscription_repository.get(session=session, user_id=user.id)

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await subscription_repository.update(
        session=session,
        obj=subscription,
        data={"next_payment_date": None},
    )
