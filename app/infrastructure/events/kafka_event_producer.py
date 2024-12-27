import json
import logging

from kafka import KafkaProducer

from app.application.events.producer import EventProducer
from app.domain.base.event import DomainEvent

log = logging.getLogger(__name__)


class KafkaEventProducer(EventProducer):
    def __init__(
        self,
        bootstrap_servers: list[str] | str,
        acks: str,
        retries: int,
        topic_prefix: str,
    ):
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks=acks,
            retries=retries,
        )
        self._topic_prefix = topic_prefix

    def _get_topic(self, event: DomainEvent) -> str:
        """Generate Kafka topic name based on event type"""
        return f"{self._topic_prefix}.{event.type.lower()}"

    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event to Kafka"""
        topic = self._get_topic(event)
        try:
            self._producer.send(topic, value=event.to_dict(), key=event.id.encode("utf-8"))
            self._producer.flush()
        except Exception as e:
            # TODO how to handle publish failures?
            log.critical(f"Failed to publish event {event.id}: {str(e)}")

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """Publish multiple domain events to Kafka"""
        try:
            for event in events:
                topic = self._get_topic(event)
                self._producer.send(topic, value=event.to_dict(), key=event.id.encode("utf-8"))
            self._producer.flush()
        except Exception as e:
            # TODO how to handle publish failures?
            log.critical(f"Failed to publish event batch: {str(e)}")

    def __del__(self) -> None:
        """Ensure proper cleanup of Kafka producer"""
        if hasattr(self, "producer"):
            self._producer.close()
