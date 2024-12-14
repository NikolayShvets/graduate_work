from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Transactions
from models.types import TransactionStatus, TransactionType
from repository.base import SQLAlchemyRepository


class TransactionRepository(SQLAlchemyRepository[Transactions]):
    async def get_last_success_payment(
        self, session: AsyncSession, subscription_id: UUID
    ) -> Transactions | None:
        query = (
            select(Transactions)
            .filter_by(
                subscription_id=subscription_id,
                type=TransactionType.PAYMENT,
                status=TransactionStatus.SUCCESS,
            )
            .order_by(Transactions.created_at.desc())
        )

        return (await session.execute(query)).scalars().first()


transaction_repository = TransactionRepository(Transactions)
