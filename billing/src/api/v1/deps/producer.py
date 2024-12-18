from collections.abc import AsyncGenerator
from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from services.producer.kafka import KafkaProducer
from settings.kafka import settings as kafka_settings


async def get_kafka_conn() -> AsyncGenerator[KafkaProducer, None]:
    conn = AIOKafkaProducer(
        bootstrap_servers=kafka_settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    async with conn:
        yield KafkaProducer(conn)


Producer = Annotated[KafkaProducer, Depends(get_kafka_conn)]
