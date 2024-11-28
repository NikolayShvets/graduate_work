from settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_TOPICS: list[str]
    KAFKA_BOOTSTRAP_SERVERS: list[str]
    KAFKA_GROUP_ID: str = "notifications"


settings = KafkaSettings()
