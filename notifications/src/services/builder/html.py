from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession

from repository.notification_template import notification_templates_repository
from schemas.message import Message, MimeType
from schemas.notification import DeliveryMethod, Notification


class FromHTMLTemplateBuilder:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def build(self, notification: Notification) -> Message:
        template = await notification_templates_repository.get_template(
            self._session,
            event_type=notification.event_type,
            delivery_method=DeliveryMethod.EMAIL,
        )

        user = notification.user

        return Message(
            recipients=[user],
            subject=template.subject,
            body=Template(template.template).render(username=user.name),
            mime_type=MimeType.HTML,
        )
