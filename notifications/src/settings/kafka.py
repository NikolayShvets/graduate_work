from pydantic import Field

from settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_TOPICS: list[str] = Field(default_factory=list)
    KAFKA_BOOTSTRAP_SERVERS: list[str] = Field(default_factory=list)
    KAFKA_GROUP_ID: str = "notifications"


settings = KafkaSettings()
