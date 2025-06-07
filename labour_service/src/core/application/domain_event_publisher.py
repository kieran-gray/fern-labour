import logging
from uuid import uuid4

from fern_labour_core.events.producer import EventProducer

from src.core.application.task_manager import TaskManager
from src.core.application.unit_of_work import UnitOfWork
from src.core.domain.domain_event.repository import DomainEventRepository

log = logging.getLogger(__name__)


class DomainEventPublisher:
    def __init__(
        self,
        domain_event_repository: DomainEventRepository,
        unit_of_work: UnitOfWork,
        event_producer: EventProducer,
        task_manager: TaskManager,
    ) -> None:
        self._domain_event_repository = domain_event_repository
        self._unit_of_work = unit_of_work
        self._event_producer = event_producer
        self._task_manager = task_manager

    def publish_batch_in_background(self) -> None:
        self._task_manager.create_task(
            self.publish_batch(), name=f"publish_batch_in_background:{uuid4()}"
        )

    async def publish_batch(self) -> None:
        log.debug("Publishing domain event batch")
        async with self._unit_of_work:
            domain_events = await self._domain_event_repository.get_unpublished()
            if not domain_events:
                log.info("No domain events to publish.")
                return

            result = await self._event_producer.publish_batch(events=domain_events)

            log.info(f"{len(result.success_ids)} domain events successfully published.")
            log.info(f"Published ids: {result.success_ids}")

            await self._domain_event_repository.mark_many_as_published(
                domain_event_ids=result.success_ids
            )

        if result.failure_ids:
            log.warning(f"{len(result.failure_ids)} domain events failed to publish.")
