import json
import logging

from kafka import KafkaProducer

from app.application.events.producer import EventProducer
from app.domain.base.event import DomainEvent
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class KafkaEventProducer(EventProducer):
    def __init__(self, settings: Settings):
        self._kafka_settings = settings.events.kafka_producer
        self._producer = KafkaProducer(
            bootstrap_servers=self._kafka_settings.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks=self._kafka_settings.acks,
            retries=self._kafka_settings.retries,
        )
        self._topic_prefix = self._kafka_settings.topic_prefix

    def _get_topic(self, event: DomainEvent) -> str:
        """Generate Kafka topic name based on event type"""
        return f"{self._topic_prefix}.{event.type.lower()}"

    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event to Kafka"""
        assert self._kafka_settings.kafka_enabled

        topic = self._get_topic(event)
        try:
            future = self._producer.send(topic, value=event.to_dict(), key=event.id.encode("utf-8"))
            await future.get(timeout=10)
        except Exception as e:
            # TODO how to handle publish failures?
            log.critical(f"Failed to publish event {event.id}: {str(e)}")

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """Publish multiple domain events to Kafka"""
        assert self._kafka_settings.kafka_enabled

        try:
            for event in events:
                topic = self._get_topic(event)
                self._producer.send(topic, value=event.to_dict(), key=event.id.encode("utf-8"))
            self._producer.flush()
        except Exception as e:
            # TODO how to handle publish failures?
            log.critical(f"Failed to publish event batch: {str(e)}")

    def __del__(self):
        """Ensure proper cleanup of Kafka producer"""
        if hasattr(self, "producer"):
            self._producer.close()
