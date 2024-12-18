from settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_BOOTSTRAP_SERVERS: list[str]


settings = KafkaSettings()
