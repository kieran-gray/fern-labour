import asyncio
import logging
import signal
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container

from app.application.events.consumer import EventConsumer
from app.infrastructure.persistence import initialize_mapping  # noqa
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.ioc.ioc_registry import get_providers
from app.setup.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConsumerRunner:
    def __init__(self, consumer: EventConsumer, container: AsyncContainer) -> None:
        self._consumer = consumer
        if hasattr(self._consumer, "set_container"):
            self._consumer.set_container(container)
        self._should_exit = False
        self._tasks: set[asyncio.Task] = set()  # type: ignore

    async def start(self) -> None:
        """Start the consumer and initialize signal handlers"""
        logger.info("Starting consumer...")

        try:
            consumer_task = asyncio.create_task(self._consumer.start())
            self._tasks.add(consumer_task)
            consumer_task.add_done_callback(self._tasks.discard)

            health_task = asyncio.create_task(self._health_check())
            self._tasks.add(health_task)
            health_task.add_done_callback(self._tasks.discard)

            while not self._should_exit:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error in consumer: {e}")
            raise
        finally:
            await self._shutdown()

    async def _health_check(self) -> None:
        """Periodic health check of the consumer"""
        while not self._should_exit:
            try:
                is_healthy = await self._consumer.is_healthy()
                if not is_healthy:
                    logger.warning("Consumer health check failed!")
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Error in health check: {e}")
                await asyncio.sleep(5)

    async def _shutdown(self) -> None:
        """Graceful shutdown of the consumer"""
        logger.info("Shutting down consumer...")

        await self._consumer.stop()

        for task in self._tasks:
            task.cancel()

        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        logger.info("Consumer shutdown complete")

    def handle_signals(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self._handle_signal(s)),  # type: ignore
            )

    async def _handle_signal(self, sig: signal.Signals) -> None:
        """Handle shutdown signals"""
        logger.info(f"Received exit signal {sig.name}...")
        self._should_exit = True


@asynccontextmanager
async def setup_container() -> AsyncIterator[AsyncContainer]:
    """Context manager for setting up and tearing down the dishka container"""

    settings: Settings = Settings.from_file()
    try:
        container = make_async_container(*get_providers(), context={Settings: settings})
        yield container
    finally:
        await container.close()


async def main(container: AsyncContainer) -> None:
    """Main entry point for the consumer script"""
    consumer = await container.get(EventConsumer, component=ComponentEnum.EVENTS)
    runner = ConsumerRunner(consumer=consumer, container=container)
    runner.handle_signals()

    try:
        await runner.start()
    except Exception as e:
        logger.error(f"Fatal error in consumer: {e}")
        sys.exit(1)


if __name__ == "__main__":

    async def run() -> None:
        async with setup_container() as container:
            await main(container)

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
