from collections.abc import AsyncGenerator

from aiokafka import AIOKafkaConsumer

from schemas.notification import Notification


class KafkaConsumer:
    def __init__(self, conn: AIOKafkaConsumer) -> None:
        self._conn = conn

    async def consume(self) -> AsyncGenerator[Notification, None]:
        async for msg in self._conn:
            yield Notification(**msg.value)
