import asyncio
import logging
import signal
import sys
from collections.abc import AsyncIterator, Coroutine
from contextlib import asynccontextmanager
from typing import Any

from dishka import AsyncContainer, make_async_container

from src.core.infrastructure.events.interfaces.consumer import EventConsumer
from src.core.infrastructure.persistence.initialize_mapping import map_all
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.ioc.ioc_registry import get_providers
from src.setup.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TaskManager:
    """Manages the lifecycle of asyncio tasks."""

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task[Coroutine[Any, Any, Any]]] = set()

    def create_task(self, coro: Coroutine[Any, Any, Any], name: str = "Task") -> None:
        """Create and manage a task."""
        task = asyncio.create_task(coro, name=name)
        task.add_done_callback(self._tasks.discard)
        self._tasks.add(task)

    async def cancel_all(self) -> None:
        """Cancel all running tasks."""
        for task in self._tasks:
            task.cancel()

        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    async def wait(self) -> None:
        """Wait for all tasks to complete."""
        await asyncio.gather(*self._tasks, return_exceptions=True)


class ConsumerRunner:
    def __init__(self, consumer: EventConsumer, container: AsyncContainer) -> None:
        self._consumer = consumer
        if hasattr(self._consumer, "set_container"):
            self._consumer.set_container(container)
        if hasattr(self._consumer, "set_event_handler_component"):
            self._consumer.set_event_handler_component(ComponentEnum.LABOUR_EVENTS.value)
        self._should_exit = asyncio.Event()
        self._task_manager: TaskManager = TaskManager()

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
async def setup_container() -> AsyncIterator[AsyncContainer]:
    """Context manager for setting up and tearing down the dishka container"""

    settings: Settings = Settings.from_file()
    container = make_async_container(*get_providers(), context={Settings: settings})
    try:
        yield container
    finally:
        await container.close()


async def main(container: AsyncContainer) -> None:
    """Main entry point for the consumer script"""
    consumer = await container.get(EventConsumer, component=ComponentEnum.EVENTS)
    runner = ConsumerRunner(consumer=consumer, container=container)
    runner.setup_signal_handlers()

    try:
        await runner.start()
    except Exception as e:
        logger.error("Fatal error in consumer.", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    map_all()

    async def run() -> None:
        async with setup_container() as container:
            await main(container)

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error("Unexpected error.", exc_info=e)
        sys.exit(1)
