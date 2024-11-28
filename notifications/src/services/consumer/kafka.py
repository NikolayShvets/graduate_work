from collections.abc import AsyncGenerator

import orjson
from aiokafka import AIOKafkaConsumer

from logger import logger
from schemas.notification import EventType, Notification


class KafkaConsumer:
    def __init__(self, conn: AIOKafkaConsumer) -> None:
        self._conn = conn

    async def consume(self) -> AsyncGenerator[Notification, None]:
        async for record in self._conn:
            if hasattr(self, f"_handle_{record.topic}"):
                yield await getattr(self, f"_handle_{record.topic}")(record.value)
            else:
                logger.warning("There is no handler for topic %s", record.topic)

    async def _create_notification(
        self, event_type: EventType, value: bytes
    ) -> Notification:
        return Notification(type=event_type, **orjson.loads(value))

    async def _handle_user_registered(self, value: bytes) -> Notification:
        return await self._create_notification(EventType.USER_REGISTERED, value)

    async def _handle_user_logged_in(self, value: bytes) -> Notification:
        return await self._create_notification(EventType.USER_LOGGED_IN, value)
