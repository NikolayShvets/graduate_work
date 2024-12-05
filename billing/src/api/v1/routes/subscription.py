from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.deps.user import User
from api.v1.deps.yookassa import YooKassa
from api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionRetrieveSchema,
)
from api.v1.schemas.transaction import TransactionCreateSchema
from models import Tariffs
from repository.subscription import subscription_repository
from repository.tariff import tariff_repository
from repository.transaction import transaction_repository
from services.yookassa.dto.amount import Amount
from services.yookassa.dto.confirmation import Confirmation
from services.yookassa.dto.payment import Payment

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
    tarrif_id: UUID,
    user: User,
) -> SubscriptionRetrieveSchema:
    """Оплатить подписку."""

    if not await tariff_repository.exists(session=session, id=tarrif_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if await subscription_repository.exists(session=session, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    tariff: Tariffs = await tariff_repository.get(session=session, id=tarrif_id)

    subscription = await subscription_repository.create(
        session=session,
        data=SubscriptionCreateSchema(
            user_id=user.id,
            tarrif_id=tarrif_id,
        ).model_dump(),
        commit=False,
    )

    payment = await yoo_kassa.create_recurrent_payment(
        amount=Amount(
            value=Decimal(tariff.price) / Decimal(100),
            currency=tariff.currency,
        ),
        confirmation=Confirmation(
            type="redirect",
            return_url="https://google.com",
        ),
        description=tariff.description,
    )

    # TODO: Мб создавать уже в callback?
    await transaction_repository.create(
        session=session,
        data=TransactionCreateSchema(
            id=payment.id,
            subscription_id=subscription.id,
        ).model_dump(),
        commit=True,
    )

    return subscription


@router.put("")
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


@router.get("/payment")
async def get_payment(yoo_kassa: YooKassa, payment_id: UUID) -> Payment:
    """Ручка нужна только для тестов."""
    return await yoo_kassa.get_payment(payment_id=payment_id)
