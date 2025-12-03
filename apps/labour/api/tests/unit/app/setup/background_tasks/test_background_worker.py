import asyncio
import logging

from dishka import AsyncContainer

from src.setup.background_tasks.background_task import BackgroundTask
from src.setup.background_tasks.background_worker import BackgroundWorker

log = logging.getLogger(__name__)


class MockBackgroundTask(BackgroundTask):
    def __init__(self, name, interval_seconds=60, max_concurrent=None):
        super().__init__(name, interval_seconds, max_concurrent)
        self.execute_count: int = 0
        self.should_raise = False

    async def execute(self, container: AsyncContainer) -> None:
        self.execute_count += 1
        if self.should_raise:
            raise ValueError("Test exception")


async def cancel_running_tasks(background_worker: BackgroundWorker) -> None:
    await background_worker._task_manager.cancel_all()


def test_can_create_background_worker(container: AsyncContainer) -> None:
    worker = BackgroundWorker(container=container)
    assert isinstance(worker, BackgroundWorker)


def test_can_start_background_worker_no_tasks(background_worker: BackgroundWorker) -> None:
    background_worker.start()


async def test_can_stop_background_worker_no_tasks(background_worker: BackgroundWorker) -> None:
    background_worker.start()
    await background_worker.stop()


async def test_can_register_task(background_worker: BackgroundWorker) -> None:
    background_worker.register(MockBackgroundTask(name="mock"))
    assert len(background_worker._background_tasks) == 1


async def test_can_register_task_with_max_concurrency(background_worker: BackgroundWorker) -> None:
    background_worker.register(MockBackgroundTask(name="mock", max_concurrent=1))
    background_worker.start()
    await asyncio.sleep(0.001)
    await background_worker.stop()
    assert background_worker._task_manager._max_concurrent["mock"] == 1


async def test_can_run_registered_task(background_worker: BackgroundWorker) -> None:
    mock_task = MockBackgroundTask(name="mock", interval_seconds=0.001)
    background_worker.register(mock_task)

    background_worker.start()
    await asyncio.sleep(0.005)
    await background_worker.stop()

    assert mock_task.execute_count >= 1


async def test_registered_task_raises_exception(background_worker: BackgroundWorker) -> None:
    mock_task = MockBackgroundTask(name="mock", interval_seconds=0.001)
    mock_task.should_raise = True
    background_worker.register(mock_task)

    background_worker.start()
    await asyncio.sleep(0.005)
    await background_worker.stop()

    assert mock_task.execute_count >= 1
