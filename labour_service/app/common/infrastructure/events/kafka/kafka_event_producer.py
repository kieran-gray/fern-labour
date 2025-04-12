import json
import logging

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from app.common.domain.event import DomainEvent
from app.common.domain.producer import EventProducer

log = logging.getLogger(__name__)


class KafkaEventProducer(EventProducer):
    """
    Kafka-based implementation of EventProducer.

    This class handles the publishing of domain events to Kafka topics,
    supporting both single-event and batch-event publishing.
    """

    def __init__(
        self,
        bootstrap_servers: list[str] | str,
        acks: str,
        retries: int,
        topic_prefix: str,
        producer: KafkaProducer | None = None,
    ):
        """
        Initialize the KafkaEventProducer.

        Args:
            bootstrap_servers: Kafka server addresses.
            acks: Acknowledgment settings for Kafka producer.
            retries: Number of retries for sending messages.
            topic_prefix: Prefix for Kafka topics.
            producer: Optional custom KafkaProducer instance.
        """
        self._producer = producer or KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else None,
            acks=acks,
            retries=retries,
        )
        self._topic_prefix = topic_prefix

    def _get_topic(self, event: DomainEvent) -> str:
        """
        Generate Kafka topic name based on event type.

        Args:
            event (DomainEvent): The domain event to publish.

        Returns:
            str: The generated Kafka topic name.
        """
        return f"{self._topic_prefix}.{event.type.lower()}"

    async def publish(self, event: DomainEvent) -> None:
        """
        Publish a single domain event to Kafka.

        Args:
            event (DomainEvent): The domain event to publish.
        """
        topic = self._get_topic(event)
        try:
            self._producer.send(topic, value=event.to_dict(), key=event.id)
            self._producer.flush()
        except KafkaTimeoutError as e:
            log.critical(
                f"KafkaTimeoutError while publishing event {event.id} to topic {topic}.", exc_info=e
            )
        except Exception as e:
            log.critical(f"Unexpected error while publishing event {event.id}", exc_info=e)

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """
        Publish multiple domain events to Kafka.

        Args:
            events (List[DomainEvent]): The list of domain events to publish.
        """
        if not events:
            log.debug("No events to publish in batch.")
            return

        try:
            for event in events:
                topic = self._get_topic(event)
                log.info(f"Queueing event for topic {topic}")
                self._producer.send(topic, value=event.to_dict(), key=event.id)

            self._producer.flush()
            log.info(f"Successfully published {len(events)} events to Kafka.")
        except KafkaTimeoutError as e:
            log.critical(
                f"KafkaTimeoutError while publishing batch of events {event.id} to topic {topic}.",
                exc_info=e,
            )
        except Exception as e:
            log.critical(
                f"Unexpected error while publishing batch of events {event.id}", exc_info=e
            )

    def close(self) -> None:
        """
        Close the Kafka producer to release resources.
        """
        if self._producer:
            try:
                log.debug("Closing Kafka producer.")
                self._producer.close()
                log.info("Kafka producer closed successfully.")
            except Exception as e:
                log.error("Error while closing Kafka producer.", exc_info=e)

    def __del__(self) -> None:
        """
        Destructor to ensure proper cleanup of Kafka producer.
        """
        self.close()
