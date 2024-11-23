from jinja2 import Template

from schemas.email import Email
from schemas.notification import Notification


class FromHTMLTemplateBuilder:
    def build(self, notification: Notification) -> list[Email]:
        return [
            Email(
                recipient=user.email,
                body=Template(notification.template).render(user=user),
            )
            for user in notification.users
        ]
