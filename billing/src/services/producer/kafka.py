from aiokafka import AIOKafkaProducer

from services.producer.schemas import Notification


class KafkaProducer:
    def __init__(self, conn: AIOKafkaProducer) -> None:
        self._conn = conn

    async def produce(self, notification: Notification) -> None:
        await self._conn.send_and_wait(
            topic=notification.event_type,
            value=notification.model_dump_json().encode("utf-8"),
        )
