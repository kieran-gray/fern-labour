import asyncio
import signal
from unittest.mock import AsyncMock, patch

from src.common.infrastructure.events.interfaces.consumer import EventConsumer
from src.run_consumer import ConsumerRunner, TaskManager


async def test_task_manager():
    """Test the TaskManager functionality."""
    task_manager = TaskManager()

    async def sample_task():
        await asyncio.sleep(0.01)
        return "Task Complete"

    # Test task creation
    task_manager.create_task(sample_task(), name="SampleTask")
    assert len(task_manager._tasks) == 1

    # Wait for tasks to complete
    await task_manager.wait()
    assert len(task_manager._tasks) == 0

    # Test task cancellation
    task_manager.create_task(sample_task(), name="SampleTaskToCancel")
    await task_manager.cancel_all()
    assert len(task_manager._tasks) == 0


async def test_consumer_runner_start_and_shutdown():
    """Test that the ConsumerRunner starts and shuts down correctly."""
    mock_consumer = AsyncMock(spec=EventConsumer)
    mock_consumer.is_healthy.return_value = True

    runner = ConsumerRunner(consumer=mock_consumer, container=AsyncMock())

    async def stop_after_delay():
        await asyncio.sleep(0.01)
        runner.stop()

    asyncio.create_task(stop_after_delay())
    await runner.start()

    # Ensure consumer start and stop were called
    mock_consumer.start.assert_called_once()
    mock_consumer.stop.assert_called_once()


async def test_consumer_runner_health_check():
    """Test the health check functionality of ConsumerRunner."""
    mock_consumer = AsyncMock(spec=EventConsumer)
    mock_consumer.is_healthy.side_effect = [True, False, Exception("Test Error")]

    runner = ConsumerRunner(consumer=mock_consumer, container=AsyncMock())

    async def stop_after_delay():
        await asyncio.sleep(0.01)
        runner.stop()

    asyncio.create_task(stop_after_delay())
    await runner.start()

    # Verify the health check logic
    assert mock_consumer.is_healthy.call_count == 1


async def test_consumer_runner_signal_handling():
    """Test signal handling in ConsumerRunner."""
    mock_consumer = AsyncMock(spec=EventConsumer)
    runner = ConsumerRunner(consumer=mock_consumer, container=AsyncMock())

    with patch("asyncio.get_event_loop") as mock_loop:
        runner.setup_signal_handlers()
        mock_loop.return_value.add_signal_handler.assert_any_call(signal.SIGTERM, runner.stop)
        mock_loop.return_value.add_signal_handler.assert_any_call(signal.SIGINT, runner.stop)
