import logging
from collections.abc import AsyncIterable
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer
from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.application.notification_service_client import NotificationServiceClient
from src.core.application.task_manager import TaskManager
from src.core.domain.domain_event.repository import DomainEventRepository
from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings

log = logging.getLogger(__name__)


class CommonApplicationProvider(Provider):
    component = ComponentEnum.DEFAULT
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def provide_task_manager(self) -> AsyncIterable[TaskManager]:
        log.debug("Creating AsyncioTaskManager")
        task_manager = AsyncioTaskManager()
        task_manager.set_max_concurrent(
            task_name_pattern="publish_batch_in_background", max_concurrent=1
        )

        yield task_manager
        log.debug("Stopping AsyncioTaskManager. Waiting for running tasks to complete.")
        await task_manager.wait()
        log.debug("AsyncioTaskManager shutdown complete.")

    @provide
    async def provide_domain_event_publisher(
        self,
        domain_event_repository: Annotated[
            DomainEventRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        unit_of_work: Annotated[UnitOfWork, FromComponent(ComponentEnum.DEFAULT)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        task_manager: Annotated[TaskManager, FromComponent(ComponentEnum.DEFAULT)],
    ) -> DomainEventPublisher:
        return DomainEventPublisher(
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            event_producer=event_producer,
            task_manager=task_manager,
        )

    @provide(scope=Scope.APP)
    def provide_notification_service_client(
        self,
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> NotificationServiceClient:
        return NotificationServiceClient(
            notification_service_url=settings.notifications.service_url
        )
