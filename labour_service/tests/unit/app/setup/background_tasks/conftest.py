import logging
from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.application.unit_of_work import UnitOfWork
from src.core.domain.domain_event.repository import DomainEventRepository
from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.setup.background_tasks.background_worker import BackgroundWorker
from tests.unit.app.application.conftest import MockDomainEventRepository, MockUnitOfWork

log = logging.getLogger(__name__)


class MockProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_domain_event_repo(self) -> DomainEventRepository:
        repo = MockDomainEventRepository()
        repo._data = {}
        return repo

    @provide
    async def provide_unit_of_work(self, domain_event_repo: DomainEventRepository) -> UnitOfWork:
        return MockUnitOfWork(repositories=[domain_event_repo])

    @provide
    async def provide_domain_event_publisher(
        self,
        domain_event_repository: DomainEventRepository,
        unit_of_work: UnitOfWork,
    ) -> DomainEventPublisher:
        return DomainEventPublisher(
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            event_producer=AsyncMock(),
            task_manager=AsyncioTaskManager(),
        )


@pytest_asyncio.fixture(scope="session")
async def container() -> AsyncIterator[AsyncContainer]:
    """Create a test dishka container."""
    container = make_async_container(MockProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture(scope="function")
async def background_worker(container: AsyncContainer) -> BackgroundWorker:
    return BackgroundWorker(container=container)
