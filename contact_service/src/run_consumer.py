import asyncio
import logging
import signal
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvloop
from dishka import AsyncContainer, make_async_container
from fern_labour_core.events.consumer import EventConsumer
from fern_labour_pub_sub.consumer import PubSubEventConsumer
from fern_labour_pub_sub.enums import ConsumerMode
from fern_labour_pub_sub.topic_handler import TopicHandler

from src.application.event_handlers.mapping import CONTACT_EVENT_HANDLER_MAPPING
from src.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.infrastructure.persistence.initialize_mapping import map_all
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.ioc.ioc_registry import get_providers
from src.setup.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConsumerRunner:
    def __init__(self, consumer: EventConsumer) -> None:
        self._consumer = consumer
        self._should_exit = asyncio.Event()
        self._task_manager: AsyncioTaskManager = AsyncioTaskManager()
        self.setup_signal_handlers()

    async def start(self) -> None:
        """Start the consumer and initialize signal handlers"""
        logger.info("Starting consumer...")
        self._task_manager.create_task(self._consumer.start(), "EventConsumer")
        self._task_manager.create_task(self._health_check(), "HealthCheck")

        await self._should_exit.wait()
        await self._shutdown()

    async def _health_check(self) -> None:
        """Periodic health check of the consumer"""
        while not self._should_exit.is_set():
            try:
                is_healthy = await self._consumer.is_healthy()
                if not is_healthy:
                    logger.warning("Consumer health check failed!")
                    self.stop()
                await asyncio.sleep(15)
            except Exception as e:
                logger.error("Error in health check.", exc_info=e)
                await asyncio.sleep(5)

    async def _shutdown(self) -> None:
        """Graceful shutdown of the consumer"""
        logger.info("Shutting down consumer...")
        await self._consumer.stop()
        await self._task_manager.cancel_all()
        logger.info("Consumer shutdown complete")

    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self.stop)

    def stop(self) -> None:
        """Stop the runner."""
        logger.info("ConsumerRunner stopping...")
        self._should_exit.set()


@asynccontextmanager
async def setup_container(settings: Settings) -> AsyncIterator[AsyncContainer]:
    """Context manager for setting up and tearing down the dishka container"""
    container = make_async_container(*get_providers(), context={Settings: settings})
    try:
        yield container
    finally:
        await container.close()


def setup_consumer(settings: Settings, container: AsyncContainer) -> PubSubEventConsumer:
    topic_handlers = [
        TopicHandler(topic, handler, ComponentEnum.DEFAULT)
        for topic, handler in CONTACT_EVENT_HANDLER_MAPPING.items()
    ]
    consumer = PubSubEventConsumer(
        project_id=settings.events.gcp.project_id,
        topic_handlers=topic_handlers,
        container=container,
        mode=ConsumerMode(settings.events.gcp.consumer_mode),
        batch_max_messages=settings.events.gcp.max_batch_size,
        idempotent=False,
    )
    return consumer


async def main() -> None:
    """Main entry point for the consumer script"""
    settings: Settings = Settings.from_file()

    async with setup_container(settings=settings) as container:
        consumer = setup_consumer(settings=settings, container=container)
        runner = ConsumerRunner(consumer=consumer)

        try:
            await runner.start()
        except Exception as e:
            logger.error("Fatal error in consumer.", exc_info=e)
            sys.exit(1)


if __name__ == "__main__":
    map_all()

    try:
        uvloop.run(main())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error("Unexpected error.", exc_info=e)
        sys.exit(1)
