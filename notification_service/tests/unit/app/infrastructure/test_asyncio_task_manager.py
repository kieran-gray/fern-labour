import logging
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio

from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager


async def mock_coro() -> str:
    return "hello"


@pytest_asyncio.fixture
async def task_manager() -> AsyncIterator[AsyncioTaskManager]:
    task_manager = AsyncioTaskManager()
    yield task_manager
    await task_manager.cancel_all()


async def test_can_create_task(task_manager: AsyncioTaskManager) -> None:
    task_manager.create_task(coro=mock_coro(), name="mock")
    assert len(task_manager._tasks) == 1


async def test_can_create_task_with_concurrency_limit(task_manager: AsyncioTaskManager) -> None:
    task_manager.set_max_concurrent(task_name_pattern="mock", max_concurrent=1)
    task_manager.create_task(coro=mock_coro(), name="mock")
    assert len(task_manager._tasks) == 1
    assert task_manager._max_concurrent["mock"] == 1


async def test_cannot_create_task_over_concurrency_limit(
    task_manager: AsyncioTaskManager, caplog: pytest.LogCaptureFixture
) -> None:
    task_manager.set_max_concurrent(task_name_pattern="mock", max_concurrent=1)
    task_manager.create_task(coro=mock_coro(), name="mock")

    module = "src.core.infrastructure.asyncio_task_manager"
    with caplog.at_level(logging.INFO, logger=module):
        task_manager.create_task(coro=mock_coro(), name="mock")

    assert "Skipping task" in caplog.text


def test_setting_max_concurrency_does_not_overwrite_semaphore(task_manager: AsyncioTaskManager):
    task_manager.set_max_concurrent(task_name_pattern="mock", max_concurrent=1)
    semaphore = task_manager._semaphores["mock"]

    task_manager.set_max_concurrent(task_name_pattern="mock", max_concurrent=1)
    new_semaphore = task_manager._semaphores["mock"]

    assert semaphore is new_semaphore
