import logging

from dishka import AsyncContainer

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.setup.background_tasks.background_task import BackgroundTask
from src.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class DomainEventPublisherTask(BackgroundTask):
    """Background task for publishing domain events."""

    async def execute(self, container: AsyncContainer) -> None:
        async with container() as request_container:
            domain_event_publisher = await request_container.get(
                DomainEventPublisher, component=ComponentEnum.DEFAULT
            )
            await domain_event_publisher.publish_batch()
