from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Plans2Services, Services2Movies, Subscriptions, Tariffs, Transactions
from models.types import TransactionStatus, TransactionType
from repository.base import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository[Subscriptions]):
    async def get_user_active_subscription(
        self, session: AsyncSession, user_id: UUID
    ) -> Subscriptions | None:
        """Получить активную подписку пользователя."""

        query = (
            select(Subscriptions)
            .filter_by(user_id=user_id)
            .options(
                joinedload(Subscriptions.tariff),
                joinedload(
                    Subscriptions.transactions.and_(
                        Transactions.status == TransactionStatus.SUCCESS
                    )
                ),
            )
        )

        subscription = (await session.execute(query)).scalars().first()

        if subscription is None:
            return None

        if not subscription.transactions:
            return None

        last_success_tr: Transactions = sorted(
            subscription.transactions, key=lambda tr: tr.created_at, reverse=True
        )[0]

        if last_success_tr.type == TransactionType.REFUND:
            return None

        is_expired = (
            last_success_tr.created_at
            + timedelta(days=subscription.tariff.get_period_in_days())
            < datetime.now()
        )

        if is_expired:
            return None

        return subscription

    async def movie_is_available(
        self,
        session: AsyncSession,
        subscription_id: UUID,
        movie_id: int,
    ) -> bool:
        """Проверить, есть ли переданный фильм в подписке."""

        movies_in_subscription_query = (
            select(Services2Movies.movie_id)
            .join(
                Plans2Services, Plans2Services.service_id == Services2Movies.service_id
            )
            .join(Tariffs, Tariffs.plan_id == Plans2Services.plan_id)
            .join(Subscriptions, Subscriptions.tariff_id == Tariffs.id)
            .where(Subscriptions.id == subscription_id)
            .distinct()
        )

        movies_in_subscription = (
            (await session.execute(movies_in_subscription_query)).scalars().all()
        )

        return movie_id in movies_in_subscription


subscription_repository = SubscriptionRepository(Subscriptions)
