import asyncio
import logging
from typing import Protocol

from dishka import AsyncContainer

log = logging.getLogger(__name__)


class BackgroundTask(Protocol):
    """Protocol for background tasks."""

    name: str
    interval_seconds: int
    max_concurrent: int | None

    def __init__(
        self, name: str, interval_seconds: int = 60, max_concurrent: int | None = None
    ) -> None:
        self.name = name
        self.interval_seconds = interval_seconds
        self.max_concurrent = max_concurrent

    async def execute(self, container: AsyncContainer) -> None:
        """Execute the background task logic."""

    async def run_periodically(self, container: AsyncContainer) -> None:
        """Run the task periodically with the specified interval."""
        try:
            while True:
                try:
                    await self.execute(container)
                except Exception as e:
                    log.error(f"Error in background task '{self.name}': {e}")
                await asyncio.sleep(self.interval_seconds)
        except asyncio.CancelledError:
            log.debug(f"Background task '{self.name}' was cancelled")
            raise
