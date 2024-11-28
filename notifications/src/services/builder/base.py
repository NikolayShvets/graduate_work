from typing import Protocol

from schemas.message import Message
from schemas.notification import Notification


class Builder(Protocol):
    def build(self, notification: Notification) -> Message: ...
