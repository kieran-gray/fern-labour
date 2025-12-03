from src.setup.background_tasks.background_task import BackgroundTask


def test_can_create_background_task():
    task = BackgroundTask(name="test", interval_seconds=60, max_concurrent=1)
    assert isinstance(task, BackgroundTask)


def test_can_create_background_task_with_defaults():
    task = BackgroundTask(name="test")
    assert isinstance(task, BackgroundTask)
