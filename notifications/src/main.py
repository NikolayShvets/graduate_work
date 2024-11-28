import asyncio

from aiokafka import AIOKafkaConsumer
from aiosmtplib import SMTP
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db import postgresql
from repository.processed_notification import processed_notifications_repository
from schemas.message import Message
from services.builder.base import Builder
from services.builder.html import FromHTMLTemplateBuilder
from services.consumer.base import Consumer
from services.consumer.kafka import KafkaConsumer
from services.sender.base import Sender
from services.sender.smtp import EmailSender
from settings.kafka import settings as kafka_settings
from settings.postgresql import settings as postgresql_settings
from settings.smtp import settings as smtp_settings


async def run_notification_process(
    consumer: Consumer, sender: Sender, builder: Builder, session: AsyncSession
) -> None:
    async for notification in consumer.consume():
        if await processed_notifications_repository.exists(
            session, notification_id=notification.id
        ):
            continue

        message: Message = await builder.build(notification)

        # TODO: Подумать над обработкой исключений
        try:
            await sender.send(message)
        except Exception:
            continue

        await consumer._conn.commit()

        await processed_notifications_repository.create(
            session, {"notification_id": notification.id}
        )


async def main() -> None:
    kafka_consumer_client = AIOKafkaConsumer(
        *kafka_settings.KAFKA_TOPICS,
        bootstrap_servers=kafka_settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=kafka_settings.KAFKA_GROUP_ID,
        enable_auto_commit=False,
    )

    smtp_client = SMTP(
        hostname=smtp_settings.SMTP_HOST,
        port=smtp_settings.SMTP_PORT,
        username=smtp_settings.SMTP_USER,
        password=smtp_settings.SMTP_PASSWORD.get_secret_value(),
        start_tls=False,
        use_tls=True,
    )

    postgresql.async_engine = create_async_engine(
        postgresql_settings.DSN,
        echo=postgresql_settings.LOG_QUERIES,
    )
    postgresql.async_session = async_sessionmaker(
        postgresql.async_engine, expire_on_commit=False
    )

    async with (
        kafka_consumer_client as kafka_conn,
        postgresql.get_async_session() as session,
    ):
        consumer = KafkaConsumer(kafka_conn)
        sender = EmailSender(smtp_client)
        builder = FromHTMLTemplateBuilder(session)

        await run_notification_process(consumer, sender, builder, session)


if __name__ == "__main__":
    asyncio.run(main())
