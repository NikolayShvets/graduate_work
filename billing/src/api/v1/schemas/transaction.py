from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base
from models.types import TransactionStatus, TransactionType


class TransactionBaseSchema(Base):
    subscription_id: UUID
    status: TransactionStatus
    type: TransactionType


class TransactionCreateSchema(TransactionBaseSchema):
    payment_id: UUID
    status: TransactionStatus = TransactionStatus.PENDING


class TransactionUpdateSchema(TransactionBaseSchema):
    pass


class TransactionRetrieveSchema(TransactionBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
