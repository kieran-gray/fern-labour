import json
import logging
from typing import Any

from dishka import AsyncContainer, Scope
from kafka import KafkaConsumer

from app.application.events.consumer import EventConsumer
from app.application.events.event_handler import EventHandler
from app.labour.application.event_handlers.mapping import EVENT_HANDLER_MAPPING
from app.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class KafkaEventConsumer(EventConsumer):
    """
    Kafka-based implementation of EventConsumer.
    """

    def __init__(
        self,
        bootstrap_servers: list[str] | str,
        group_id: str,
        topic_prefix: str,
        consumer: KafkaConsumer | None = None,
    ):
        """
        Initialize KafkaEventConsumer.

        Args:
            bootstrap_servers: Kafka bootstrap servers.
            group_id: Kafka consumer group ID.
            topic_prefix: Prefix for Kafka topics.
            consumer: Optional pre-configured KafkaConsumer.
        """
        self._consumer = consumer or KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v),
            enable_auto_commit=False,
        )
        self._handlers: dict[str, type[EventHandler]] = {
            f"{topic_prefix}.{topic}": handler for topic, handler in EVENT_HANDLER_MAPPING.items()
        }
        self._running = False
        self._container: AsyncContainer | None = None
        self._subscribe_to_topics()

    def set_container(self, container: AsyncContainer) -> None:
        """
        The consumer is running in a Dishka async container with scope=APP.

        Dependencies with scope=APP are created once and reused whenever requested in the container.

        Dependencies with scope=Request, shorter lived dependencies like database sessions or
        anything that depends on a database session, need to be created in a container with
        scope=request.

        For FastAPI routes this is handled with the Dishka-FastAPI integration, but here we need to
        handle it ourselves.

        So, we are going to store the container (which is scope=app), then when we need to handle
        a batch of events, we will start a child container with scope=request.

        Args:
            container: AsyncContainer with scope=APP.
        """
        self._container = container

    def _subscribe_to_topics(self) -> None:
        """
        Subscribe to topics specified in the handler mapping.
        """
        if topics := list(self._handlers.keys()):
            self._consumer.subscribe(topics=topics)
            log.info(f"Subscribed to topics: {topics}")
        else:
            log.warning("No topics to subscribe to.")

    async def _handle_messages(self, messages: dict[Any, list[Any]]) -> None:
        """
        Handle a batch of Kafka messages.

        Args:
            messages: Messages partitioned by topic and partition.
        """
        if not self._container:
            log.error("Dependency injection container not set. Cannot process messages.")
            return

        async with self._container(scope=Scope.REQUEST) as request_container:
            for partition_messages in messages.values():
                for message in partition_messages:
                    await self._process_message(message, request_container)

    async def _process_message(self, message: Any, request_container: AsyncContainer) -> None:
        """
        Process a single Kafka message.

        Args:
            message: The Kafka message to process.
            request_container: A container scoped for handling the message.
        """
        log.info(f"Received message with topic: {message.topic}")
        handler_cls = self._handlers.get(message.topic)

        if not handler_cls:
            log.error(f"No handler found for topic: {message.topic}")
            return

        try:
            event_handler = await request_container.get(handler_cls, component=ComponentEnum.EVENTS)
            await event_handler.handle(message.value)
            self._consumer.commit()
            log.info(f"Committed offset for topic: {message.topic}")
        except Exception as e:
            log.exception(f"Error processing message from topic {message.topic}.", exc_info=e)

    async def start(self) -> None:
        """
        Start the Kafka consumer and process messages.
        """
        if not self._handlers:
            log.error("No event handlers registered.")
            return await self.stop()

        self._running = True
        log.info("KafkaEventConsumer started.")
        while self._running:
            try:
                messages = self._consumer.poll(timeout_ms=1000)
                if messages:
                    log.info(f"Handling {len(messages)} messages.")
                    await self._handle_messages(messages=messages)
            except Exception as e:
                log.exception("Error during message polling.", exc_info=e)

    async def stop(self) -> None:
        """
        Stop the Kafka consumer.
        """
        self._running = False
        if self._consumer:
            self._consumer.close()

        log.info("KafkaEventConsumer stopped.")

    async def is_healthy(self) -> bool:
        """
        Check if the Kafka consumer is healthy.

        Returns:
            True if healthy, otherwise False.
        """
        if not self._consumer:
            log.warning("Kafka consumer is not initialized.")
            return False
        try:
            return all(self._consumer.assignment())
        except Exception as e:
            log.exception("Error checking Kafka consumer health.", exc_info=e)
            return False
