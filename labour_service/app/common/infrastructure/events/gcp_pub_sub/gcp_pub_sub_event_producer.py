import json
import logging

from google.api_core.exceptions import DeadlineExceeded
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.futures import Future

from app.application.events.producer import EventProducer
from app.domain.base.event import DomainEvent

log = logging.getLogger(__name__)

FUTURE_TIMEOUT_SECONDS = 30


class PubSubEventProducer(EventProducer):
    """
    Google Pub/Sub-based implementation of EventProducer.

    This class handles the publishing of domain events to Pub/Sub topics,
    supporting both single-event and batch-event publishing.
    """

    def __init__(
        self,
        project_id: str,
        retries: int = 3,
        publisher: pubsub_v1.PublisherClient | None = None,
    ):
        """
        Initialize the PubSubEventProducer.

        Args:
            project_id: Google Cloud project ID.
            topic_prefix: Prefix for Pub/Sub topics.
            retries: Number of retries for failed publish operations.
            publisher: Optional custom PublisherClient instance.
        """
        self._publisher = publisher or pubsub_v1.PublisherClient()
        self._project_id = project_id
        self._retries = retries

    def _get_topic_path(self, event: DomainEvent) -> str:
        """
        Generate full Pub/Sub topic path based on event type.

        Args:
            event: The domain event to publish.

        Returns:
            The generated Pub/Sub topic path.
        """
        return self._publisher.topic_path(self._project_id, event.type.lower())

    def _serialize_event(self, event: DomainEvent) -> bytes:
        """
        Serialize event data to bytes for Pub/Sub.

        Args:
            event: The domain event to serialize.

        Returns:
            Serialized event data as bytes.
        """
        return json.dumps(event.to_dict()).encode("utf-8")

    async def publish(self, event: DomainEvent) -> None:
        """
        Publish a single domain event to Pub/Sub.

        Args:
            event: The domain event to publish.
        """
        topic_path = self._get_topic_path(event)
        data = self._serialize_event(event)

        attributes = {"event_id": event.id}

        try:
            future: Future = self._publisher.publish(topic_path, data=data, **attributes)
            message_id = future.result(timeout=FUTURE_TIMEOUT_SECONDS)
            log.debug(f"Published event {event.id} to {topic_path} with message ID {message_id}")
        except DeadlineExceeded as e:
            log.critical(
                f"Timeout error while publishing event {event.id} to topic {topic_path}.",
                exc_info=e,
            )
        except Exception as e:
            log.critical(f"Unexpected error while publishing event {event.id}", exc_info=e)

    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """
        Publish multiple domain events to Pub/Sub.

        Args:
            events: The list of domain events to publish.
        """
        if not events:
            log.debug("No events to publish in batch.")
            return

        futures = []

        try:
            for event in events:
                topic_path = self._get_topic_path(event)
                data = self._serialize_event(event)
                attributes = {"event_id": event.id}

                log.debug(f"Queueing event {event.id} for topic {topic_path}")
                future: Future = self._publisher.publish(topic_path, data=data, **attributes)
                futures.append((future, event.id, topic_path))

            for future, event_id, topic_path in futures:
                try:
                    message_id = future.result(timeout=FUTURE_TIMEOUT_SECONDS)
                    log.debug(
                        f"Published event {event_id} to {topic_path} with message ID {message_id}"
                    )
                except Exception as e:
                    log.error(f"Failed to publish event {event_id}: {str(e)}")

            log.info(f"Successfully published {len(events)} events to Pub/Sub.")
        except Exception as e:
            log.critical("Unexpected error while publishing batch of events", exc_info=e)

    def close(self) -> None:
        """
        Close the Pub/Sub publisher to release resources.
        """
        if self._publisher:
            try:
                log.debug("Closing Pub/Sub publisher.")
                self._publisher.close()
                log.info("Pub/Sub publisher closed successfully.")
            except Exception as e:
                log.error("Error while closing Pub/Sub publisher.", exc_info=e)

    def __del__(self) -> None:
        """
        Destructor to ensure proper cleanup of Pub/Sub publisher.
        """
        self.close()
