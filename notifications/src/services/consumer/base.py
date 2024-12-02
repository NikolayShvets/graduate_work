from collections.abc import AsyncGenerator
from typing import Protocol

from schemas.notification import Notification


class Consumer(Protocol):
    async def consume(self) -> AsyncGenerator[Notification, None]: ...
