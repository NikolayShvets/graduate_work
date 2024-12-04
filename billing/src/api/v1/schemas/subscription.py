from datetime import datetime
from uuid import UUID

from api.v1.schemas.base import Base


class SubscriptionBaseSchema(Base):
    user_id: UUID
    tarrif_id: UUID


class SubscriptionCreateSchema(SubscriptionBaseSchema):
    pass


class SubscriptionUpdateSchema(SubscriptionBaseSchema):
    pass


class SubscriptionRetrieveSchema(SubscriptionBaseSchema):
    id: UUID
    next_payment_date: datetime
    created_at: datetime
    updated_at: datetime
