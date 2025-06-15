from datetime import UTC, datetime
from typing import Self
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fern_labour_core.events.event import DomainEvent
from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.domain.domain_event.repository import DomainEventRepository
from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.core.infrastructure.security.rate_limiting.in_memory import InMemoryRateLimiter
from src.core.infrastructure.security.rate_limiting.interface import RateLimiter
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.contraction_service import ContractionService
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.repository import LabourRepository
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionAccessLevel, SubscriptionStatus
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.repository import UserRepository
from src.user.domain.value_objects.user_id import UserId


class MockUserRepository(UserRepository):
    _data = {}

    async def save(self, user: User) -> None:
        self._data[user.id_.value] = user

    async def delete(self, user: User) -> None:
        self._data.pop(user.id_.value)

    async def get_by_id(self, user_id: UserId) -> User | None:
        return self._data.get(user_id.value, None)

    async def get_by_ids(self, user_ids: list[UserId]) -> list[User]:
        users = []
        for user_id in user_ids:
            if user := self._data.get(user_id.value, None):
                users.append(user)
        return users


class MockLabourRepository(LabourRepository):
    _data = {}
    _changes = {}

    async def save(self, labour: Labour) -> None:
        self._changes[labour.id_.value] = labour

    async def delete(self, labour: Labour) -> None:
        self._changes.pop(labour.id_.value)

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        return self._data.get(labour_id.value, None)

    async def get_labours_by_birthing_person_id(self, birthing_person_id: UserId):
        return [
            labour
            for labour in self._data.values()
            if labour.birthing_person_id == birthing_person_id
        ]

    async def get_active_labour_by_birthing_person_id(self, birthing_person_id: UserId):
        return next(
            (
                labour
                for labour in self._data.values()
                if labour.birthing_person_id == birthing_person_id
            ),
            None,
        )

    async def get_active_labour_id_by_birthing_person_id(self, birthing_person_id: UserId):
        return next(
            (
                labour.id_
                for labour in self._data.values()
                if labour.birthing_person_id == birthing_person_id
            ),
            None,
        )

    async def get_birthing_person_id_for_labour(self, labour_id: LabourId) -> UserId | None:
        labour = self._data.get(labour_id.value, None)
        if not labour:
            return labour
        return labour.birthing_person_id


class MockSubscriptionRepository(SubscriptionRepository):
    _data: dict[str, Subscription] = {}
    _changes: dict[str, Subscription] = {}

    async def save(self, subscription: Subscription) -> None:
        self._changes[subscription.id_.value] = subscription

    async def delete(self, subscription: Subscription) -> None:
        self._changes.pop(subscription.id_.value)

    async def get_by_id(self, subscription_id: SubscriptionId) -> Subscription | None:
        return self._data.get(subscription_id.value, None)

    async def get_by_ids(self, subscription_ids: list[SubscriptionId]) -> list[Subscription]:
        subscriptions = []
        for subscription_id in subscription_ids:
            if subscription := self._data.get(subscription_id.value, None):
                subscriptions.append(subscription)
        return subscriptions

    async def filter(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: UserId | None = None,
        birthing_person_id: UserId | None = None,
        subscription_status: SubscriptionStatus | None = None,
        access_level: SubscriptionAccessLevel | None = None,
    ) -> list[Subscription]:
        subscriptions = []
        for subscription in self._data.values():
            if labour_id and subscription.labour_id != labour_id:
                continue
            if subscriber_id and subscription.subscriber_id != subscriber_id:
                continue
            if birthing_person_id and subscription.birthing_person_id != birthing_person_id:
                continue
            if subscription_status and subscription.status is not subscription_status:
                continue
            if access_level and subscription.access_level is not access_level:
                continue
            subscriptions.append(subscription)
        return subscriptions

    async def filter_one_or_none(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: UserId | None = None,
        birthing_person_id: UserId | None = None,
        subscription_status: SubscriptionStatus | None = None,
        access_level: SubscriptionAccessLevel | None = None,
    ) -> Subscription | None:
        found_subscription = None
        for subscription in self._data.values():
            if labour_id and subscription.labour_id != labour_id:
                continue
            if subscriber_id and subscription.subscriber_id != subscriber_id:
                continue
            if birthing_person_id and subscription.birthing_person_id != birthing_person_id:
                continue
            if subscription_status and subscription.status is not subscription_status:
                continue
            if access_level and subscription.access_level is not access_level:
                continue
            if found_subscription:
                raise ValueError("Multiple results found")
            found_subscription = subscription
        return found_subscription


class MockDomainEventRepository(DomainEventRepository):
    _data: dict[str, tuple[DomainEvent, datetime | None]] = {}
    _changes: dict[str, tuple[DomainEvent, datetime | None]] = {}

    async def commit(self) -> None:
        self._data.update(self._changes)

    async def save(self, domain_event: DomainEvent) -> None:
        self._changes[domain_event.id] = (domain_event, None)

    async def save_many(self, domain_events: list[DomainEvent]):
        for domain_event in domain_events:
            self._changes[domain_event.id] = (domain_event, None)

    async def get_unpublished(self, limit=100) -> list[DomainEvent]:
        unpublished = []
        for domain_event, published in self._changes.values():
            if not published:
                unpublished.append(domain_event)
        return unpublished

    async def mark_as_published(self, domain_event_id: str) -> None:
        domain_event = self._changes.get(domain_event_id)
        domain_event[1] = datetime.now(UTC)

    async def mark_many_as_published(self, domain_event_ids: list[str]) -> None:
        for domain_event_id in domain_event_ids:
            self.mark_as_published(domain_event_id)


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def labour_repo() -> LabourRepository:
    repo = MockLabourRepository()
    repo._data = {}
    repo._changes = {}
    return repo


@pytest_asyncio.fixture
async def subscription_repo() -> SubscriptionRepository:
    repo = MockSubscriptionRepository()
    repo._data = {}
    repo._changes = {}
    return repo


@pytest_asyncio.fixture
async def domain_event_repo() -> DomainEventRepository:
    repo = MockDomainEventRepository()
    repo._data = {}
    repo._changes = {}
    return repo


class MockUnitOfWork(UnitOfWork):
    def __init__(self, repositories) -> None:
        self._repositories: list = repositories

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        except Exception:
            raise
        return None

    async def commit(self) -> None:
        for repository in self._repositories:
            repository._data.update(repository._changes)

    async def rollback(self) -> None:
        for repository in self._repositories:
            repository._changes = {}


@pytest_asyncio.fixture
async def unit_of_work(
    labour_repo: LabourRepository,
    domain_event_repo: DomainEventRepository,
    subscription_repo: SubscriptionRepository,
) -> UnitOfWork:
    return MockUnitOfWork(repositories=[labour_repo, domain_event_repo, subscription_repo])


class MockTokenGenerator(TokenGenerator):
    def generate(self, input: str) -> str:
        return input

    def validate(self, id: str, token: str):
        return token == id


@pytest.fixture
def token_generator() -> TokenGenerator:
    return MockTokenGenerator()


@pytest.fixture
def rate_limiter() -> RateLimiter:
    return InMemoryRateLimiter()


@pytest_asyncio.fixture
async def domain_event_publisher(
    domain_event_repo: DomainEventRepository, unit_of_work: UnitOfWork
) -> DomainEventPublisher:
    return DomainEventPublisher(
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        event_producer=AsyncMock(),
        task_manager=AsyncioTaskManager(),
    )


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)


@pytest_asyncio.fixture
async def labour_service(
    labour_repo: LabourRepository,
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    domain_event_publisher: DomainEventPublisher,
) -> LabourService:
    return LabourService(
        labour_repository=labour_repo,
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        domain_event_publisher=domain_event_publisher,
    )


@pytest_asyncio.fixture
async def contraction_service(
    labour_repo: LabourRepository,
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    domain_event_publisher: DomainEventPublisher,
) -> ContractionService:
    return ContractionService(
        labour_repository=labour_repo,
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        domain_event_publisher=domain_event_publisher,
    )


@pytest_asyncio.fixture
async def labour_query_service(
    labour_repo: LabourRepository,
) -> LabourQueryService:
    return LabourQueryService(
        labour_repository=labour_repo,
    )


@pytest_asyncio.fixture
async def subscription_authorization_service(
    subscription_repo: SubscriptionRepository,
) -> SubscriptionAuthorizationService:
    return SubscriptionAuthorizationService(subscription_repository=subscription_repo)


@pytest_asyncio.fixture
async def subscription_service(
    labour_query_service: LabourQueryService,
    subscription_repo: SubscriptionRepository,
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    token_generator: TokenGenerator,
    domain_event_publisher: DomainEventPublisher,
) -> SubscriptionService:
    return SubscriptionService(
        labour_query_service=labour_query_service,
        subscription_repository=subscription_repo,
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        token_generator=token_generator,
        domain_event_publisher=domain_event_publisher,
    )


@pytest_asyncio.fixture
async def subscription_query_service(
    subscription_repo: SubscriptionRepository,
    subscription_authorization_service: SubscriptionAuthorizationService,
) -> SubscriptionQueryService:
    return SubscriptionQueryService(
        subscription_repository=subscription_repo,
        subscription_authorization_service=subscription_authorization_service,
    )


@pytest_asyncio.fixture
async def subscription_management_service(
    subscription_repo: SubscriptionRepository,
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    subscription_authorization_service: SubscriptionAuthorizationService,
    domain_event_publisher: DomainEventPublisher,
) -> SubscriptionManagementService:
    return SubscriptionManagementService(
        subscription_repository=subscription_repo,
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        subscription_authorization_service=subscription_authorization_service,
        domain_event_publisher=domain_event_publisher,
    )
