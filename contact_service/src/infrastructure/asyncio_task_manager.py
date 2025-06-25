import asyncio
import logging
from collections import defaultdict
from collections.abc import Coroutine
from typing import Any

from src.application.task_manager import TaskManager

log = logging.getLogger(__name__)


class AsyncioTaskManager(TaskManager):
    """Manages the lifecycle of asyncio tasks."""

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task[Coroutine[Any, Any, Any]]] = set()
        self._semaphores: dict[str, asyncio.Semaphore] = {}
        self._running_counts: dict[str, int] = defaultdict(int)
        self._max_concurrent: dict[str, int] = {}

    def set_max_concurrent(self, task_name_pattern: str, max_concurrent: int) -> None:
        """Set maximum concurrent tasks for a specific task name pattern."""
        task_name = self._get_task_name(name=task_name_pattern)

        if task_name in self._semaphores:
            return

        self._max_concurrent[task_name] = max_concurrent
        self._semaphores[task_name] = asyncio.Semaphore(max_concurrent)

    def create_task(self, coro: Coroutine[Any, Any, Any], name: str = "Task") -> None:
        """Create and manage a task with optional concurrency control."""
        task_name = self._get_task_name(name=name)

        if task_name in self._semaphores:
            current_running = self._running_counts[task_name]
            max_allowed = self._max_concurrent[task_name]

            if current_running >= max_allowed:
                log.info(f"Skipping task '{name}' - concurrency limit reached")
                coro.close()
                return

            self._running_counts[task_name] += 1
            wrapped_coro = self._wrap_with_semaphore(coro, task_name)
            task = asyncio.create_task(wrapped_coro, name=name)
        else:
            task = asyncio.create_task(coro, name=name)

        task.add_done_callback(self._tasks.discard)
        self._tasks.add(task)

    def _get_task_name(self, name: str) -> str:
        """Get task name from provided name."""
        return name.split(":")[0]

    async def _wrap_with_semaphore(self, coro: Coroutine[Any, Any, Any], task_name: str) -> Any:
        """Wrap coroutine with semaphore control."""
        semaphore = self._semaphores[task_name]
        try:
            async with semaphore:
                return await coro
        finally:
            self._running_counts[task_name] -= 1

    async def cancel_all(self) -> None:
        """Cancel all running tasks."""
        for task in self._tasks:
            task.cancel()

        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    async def wait(self) -> None:
        """Wait for all tasks to complete."""
        await asyncio.gather(*self._tasks, return_exceptions=True)
