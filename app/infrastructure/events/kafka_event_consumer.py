__all__ = "initialize_mapping"

import json
import logging
from typing import Any

from dishka import AsyncContainer, Scope
from kafka import KafkaConsumer

from app.application.events.consumer import EventConsumer
from app.application.events.event_handlers.mapping import EVENT_HANDLER_MAPPING
from app.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class KafkaEventConsumer(EventConsumer):
    def __init__(self, bootstrap_servers: list[str] | str, group_id: str):
        self._consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v),
            enable_auto_commit=False,
        )
        self._handlers = EVENT_HANDLER_MAPPING
        self._running = False
        self._subscribe()

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
        """
        self._container: AsyncContainer = container

    def _subscribe(self) -> None:
        self._consumer.subscribe(topics=list(self._handlers.keys()))

    async def _handle_messages(self, messages: dict[Any, list[Any]]) -> None:
        async with self._container(scope=Scope.REQUEST) as request_container:
            for partition_messages in messages.values():
                for message in partition_messages:
                    log.info(f"Received message: {message.topic} - {message.value}")
                    event_handler = self._handlers.get(message.topic)
                    if not event_handler:
                        log.error(f"No event handler found for topic {message.topic}")
                        continue
                    try:
                        concrete_handler = await request_container.get(
                            event_handler, component=ComponentEnum.EVENTS
                        )
                        await concrete_handler.handle(message.value)
                        self._consumer.commit()
                    except Exception as e:
                        log.error(f"Error handling message: {e}")

    async def start(self) -> None:
        if not self._handlers:
            log.error("No event handlers registered")
            await self.stop()

        self._running = True
        while self._running:
            messages = self._consumer.poll(timeout_ms=1000)
            if not messages:
                continue

            log.info(f"Handling {len(messages)} messages.")
            await self._handle_messages(messages=messages)

    async def stop(self) -> None:
        self._running = False
        if self._consumer:
            self._consumer.close()

    async def is_healthy(self) -> bool:
        if not self._consumer:
            return False
        try:
            return all(self._consumer.assignment())
        except Exception:
            return False
