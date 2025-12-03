from dishka import AsyncContainer

from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.setup.background_tasks.background_task import BackgroundTask


class BackgroundWorker:
    def __init__(self, container: AsyncContainer):
        self._app_container = container
        self._task_manager = AsyncioTaskManager()
        self._background_tasks: list[BackgroundTask] = []

    def register(self, background_task: BackgroundTask) -> None:
        """Register a background task to be started when the worker starts."""
        self._background_tasks.append(background_task)

    def start(self) -> None:
        """Start all registered background tasks."""
        for task in self._background_tasks:
            if task.max_concurrent:
                self._task_manager.set_max_concurrent(
                    task_name_pattern=task.name, max_concurrent=task.max_concurrent
                )
            self._task_manager.create_task(
                task.run_periodically(self._app_container), name=task.name
            )

    async def stop(self) -> None:
        """Stop all running background tasks."""
        await self._task_manager.cancel_all()
