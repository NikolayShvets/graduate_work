from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import DeliveryMethods, EventTypes, NotificationTemplates, Templates
from repository.base import SQLAlchemyRepository
from schemas.notification import DeliveryMethod, EventType


class NotificationTemplatesRepository(SQLAlchemyRepository[NotificationTemplates]):
    async def get_template(
        self,
        session: AsyncSession,
        event_type: EventType,
        delivery_method: DeliveryMethod,
    ) -> Templates:
        query = (
            select(NotificationTemplates)
            .join(EventTypes)
            .join(DeliveryMethods)
            .where(
                EventTypes.type == event_type, DeliveryMethods.method == delivery_method
            )
            .options(joinedload(NotificationTemplates.template))
        )

        return (await session.execute(query)).scalars().first().template


notification_templates_repository = NotificationTemplatesRepository(
    NotificationTemplates
)
