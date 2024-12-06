from aiokafka import AIOKafkaProducer
from settings.kafka import settings
from notifications.schemas.notification import Notification


class KafkaProducer:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_message(self, topic: str, message: Notification):
        await self.producer.send_and_wait(topic, value=message.json().encode('utf-8'))


kafka_producer = KafkaProducer()
