from collections.abc import Coroutine
from typing import Any, Protocol


class TaskManager(Protocol):
    """Manages background tasks."""

    def set_max_concurrent(self, task_name_pattern: str, max_concurrent: int) -> None:
        """Set maximum concurrent tasks for a specific task name pattern."""

    def create_task(self, coro: Coroutine[Any, Any, Any], name: str = "Task") -> None:
        """Create and manage a task."""

    async def cancel_all(self) -> None:
        """Cancel all running tasks."""

    async def wait(self) -> None:
        """Wait for all tasks to complete."""
