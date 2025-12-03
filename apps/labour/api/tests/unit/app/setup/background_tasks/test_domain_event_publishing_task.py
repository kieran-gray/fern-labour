from src.setup.background_tasks.background_worker import BackgroundWorker
from src.setup.background_tasks.domain_event_publisher_task import DomainEventPublisherTask


class MockDomainEventPublisherTask(DomainEventPublisherTask):
    async def run_periodically(self, container):
        return await self.execute(container)


async def test_can_run_background_publisher_task(background_worker: BackgroundWorker) -> None:
    task = MockDomainEventPublisherTask(name="domain_event_publisher_task")
    background_worker.register(task)
    background_worker.start()
    await background_worker._task_manager.wait()
    await background_worker.stop()
