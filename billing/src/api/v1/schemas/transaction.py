from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base
from models.types import TransactionStatus


class TransactionBaseSchema(Base):
    subscription_id: UUID
    status: TransactionStatus


class TransactionCreateSchema(TransactionBaseSchema):
    id: UUID
    status: TransactionStatus = TransactionStatus.PENDING


class TransactionUpdateSchema(TransactionBaseSchema):
    pass


class TransactionRetrieveSchema(TransactionBaseSchema):
    created_at: datetime
    updated_at: datetime
