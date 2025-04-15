import json
import logging
from typing import Type
import asyncio

from dishka import AsyncContainer, Scope
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture
from concurrent.futures import ThreadPoolExecutor

from app.application.events.consumer import EventConsumer
from app.application.events.event_handler import EventHandler
from app.application.events.event_handlers.mapping import EVENT_HANDLER_MAPPING
from app.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class PubSubEventConsumer(EventConsumer):
    """
    Google Pub/Sub-based implementation of EventConsumer.
    """

    def __init__(
        self,
        project_id: str,
        subscription_prefix: str,
        topic_prefix: str,
        subscriber: pubsub_v1.SubscriberClient | None = None,
    ):
        """
        Initialize PubSubEventConsumer.

        Args:
            project_id: Google Cloud project ID.
            subscription_prefix: Prefix for Pub/Sub subscriptions.
            topic_prefix: Prefix for Pub/Sub topics.
            subscriber: Optional pre-configured SubscriberClient.
        """
        self._project_id = project_id
        self._subscription_prefix = subscription_prefix
        self._subscriber = subscriber or pubsub_v1.SubscriberClient()
        self._handlers: dict[str, Type[EventHandler]] = {
            f"{topic_prefix}.{topic}": handler for topic, handler in EVENT_HANDLER_MAPPING.items()
        }
        self._running = False
        self._container: AsyncContainer | None = None
        self._streaming_pull_futures: list[StreamingPullFuture] = []
        self._executor = ThreadPoolExecutor(max_workers=10)

    def set_container(self, container: AsyncContainer) -> None:
        """
        Set the dependency injection container.

        Args:
            container: AsyncContainer with scope=APP.
        """
        self._container = container

    def _get_subscription_path(self, topic: str) -> str:
        """
        Get the full subscription path for a topic.
        
        Args:
            topic: The topic name.
            
        Returns:
            Full subscription path.
        """
        subscription_id = f"{self._subscription_prefix}.{topic.split('.')[-1]}"
        return self._subscriber.subscription_path(self._project_id, subscription_id)

    async def _process_message(self, message: Message) -> None:
        """
        Process a single Pub/Sub message.

        Args:
            message: The Pub/Sub message to process.
        """
        if not self._container:
            log.error("Dependency injection container not set. Cannot process messages.")
            message.nack()
            return
        
        topic_name = message.topic
        log.info(f"Received message from topic: {topic_name}")
        
        topic_parts = topic_name.split('/')
        short_topic = topic_parts[-1]
        full_topic = next((t for t in self._handlers.keys() if t.endswith(short_topic)), None)
        
        if not full_topic:
            log.error(f"No handler found for topic: {short_topic}")
            message.nack()
            return

        handler_cls = self._handlers.get(full_topic)
        if not handler_cls:
            log.error(f"No handler found for topic: {full_topic}")
            message.nack()
            return

        try:
            data = json.loads(message.data.decode("utf-8"))
            
            async with self._container(scope=Scope.REQUEST) as request_container:
                event_handler = await request_container.get(handler_cls, component=ComponentEnum.EVENTS)
                await event_handler.handle(data)
                
            message.ack()
            log.info(f"Successfully processed message from topic: {full_topic}")
        except Exception as e:
            log.exception(f"Error processing message from topic {full_topic}.", exc_info=e)
            message.nack()

    def _message_callback(self, message: Message) -> None:
        """
        Callback function for received messages.
        Bridges the sync callback to async processing.

        Args:
            message: The received Pub/Sub message.
        """
        import asyncio
        
        if not self._running:
            message.nack()
            return

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self._process_message(message))
        except Exception as e:
            log.exception("Error in message callback", exc_info=e)
            message.nack()
        finally:
            loop.close()

    async def start(self) -> None:
        """
        Start the Pub/Sub consumer and begin processing messages.
        """
        if not self._handlers:
            log.error("No event handlers registered.")
            return await self.stop()

        self._running = True
        log.info("PubSubEventConsumer started.")

        for topic in self._handlers.keys():
            topic_short_name = topic.split('.')[-1]
            subscription_path = self._get_subscription_path(topic_short_name)
            
            log.info(f"Subscribing to {subscription_path}")
            
            streaming_pull_future = self._subscriber.subscribe(
                subscription=subscription_path,
                callback=self._message_callback,
            )
            self._streaming_pull_futures.append(streaming_pull_future)

        while self._running:
            await asyncio.sleep(1)

    async def stop(self) -> None:
        """
        Stop the Pub/Sub consumer.
        """
        self._running = False
        
        for future in self._streaming_pull_futures:
            future.cancel()
        
        self._streaming_pull_futures = []
        
        if self._subscriber:
            self._subscriber.close()

        self._executor.shutdown(wait=True)

        log.info("PubSubEventConsumer stopped.")

    async def is_healthy(self) -> bool:
        """
        Check if the Pub/Sub consumer is healthy.

        Returns:
            True if healthy, otherwise False.
        """
        if not self._subscriber:
            log.warning("Pub/Sub subscriber is not initialized.")
            return False
            
        try:
            for future in self._streaming_pull_futures:
                if future.cancelled() or future.done():
                    return False
            return self._running and len(self._streaming_pull_futures) > 0
        except Exception as e:
            log.exception("Error checking Pub/Sub consumer health.", exc_info=e)
            return False
