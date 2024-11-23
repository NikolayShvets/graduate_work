import asyncio

from aiokafka import AIOKafkaConsumer
from aiosmtplib import SMTP
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db import postgresql
from repository.processed_notification import processed_notifications_repository
from services.builder.html import FromHTMLTemplateBuilder
from services.consumer.kafka import KafkaConsumer
from services.sender.smtp import EmailSender
from settings.kafka import settings as kafka_settings
from settings.postgresql import settings as postgresql_settings
from settings.smtp import settings as smtp_settings


async def run_notification_process(
    kafka_conn: AIOKafkaConsumer,
    smpt_conn: SMTP,
    session: AsyncSession,
) -> None:
    consumer = KafkaConsumer(kafka_conn)
    sender = EmailSender(smpt_conn)
    builder = FromHTMLTemplateBuilder()

    async for notification in consumer.consume():
        if await processed_notifications_repository.exists(
            session, notification_id=notification.id
        ):
            continue

        tasks = [sender.send(email) for email in builder.build(notification)]
        await asyncio.gather(*tasks)

        await processed_notifications_repository.create(
            session, {"notification_id": notification.id}
        )


async def main() -> None:
    kafka_consumer_client = AIOKafkaConsumer(
        kafka_settings.KAFKA_TOPICS,
        bootstrap_servers=kafka_settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=kafka_settings.KAFKA_GROUP_ID,
    )

    smtp_client = SMTP(
        smtp_settings.SMTP_HOST,
        smtp_settings.SMTP_PORT,
        smtp_settings.SMTP_USER,
        smtp_settings.SMTP_PASSWORD.get_secret_value(),
    )

    postgresql.async_engine = create_async_engine(
        postgresql_settings.DSN,
        echo=postgresql_settings.LOG_QUERIES,
    )
    postgresql.async_session = async_sessionmaker(
        postgresql.async_engine, expire_on_commit=False
    )

    pg_session = await postgresql.get_async_session()

    async with (
        kafka_consumer_client as kafka_conn,
        smtp_client as smtp_conn,
        pg_session as session,
    ):
        await run_notification_process(kafka_conn, smtp_conn, session)


if __name__ == "__main__":
    asyncio.run(main())
