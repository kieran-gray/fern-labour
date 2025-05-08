from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fakeredis import FakeValkey

from src.core.infrastructure.security.rate_limiting.interface import RateLimiter
from src.core.infrastructure.security.rate_limiting.redis import RedisRateLimiter
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

    async def save(self, labour: Labour) -> None:
        self._data[labour.id_.value] = labour

    async def delete(self, labour: Labour) -> None:
        self._data.pop(labour.id_.value)

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

    async def get_birthing_person_id_for_labour(self, labour_id: LabourId) -> UserId | None:
        labour = self._data.get(labour_id.value, None)
        if not labour:
            return labour
        return labour.birthing_person_id


class MockSubscriptionRepository(SubscriptionRepository):
    _data: dict[str, Subscription] = {}

    async def save(self, subscription: Subscription) -> None:
        self._data[subscription.id_.value] = subscription

    async def delete(self, subscription: Subscription) -> None:
        self._data.pop(subscription.id_.value)

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


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def labour_repo() -> LabourRepository:
    repo = MockLabourRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def subscription_repo() -> SubscriptionRepository:
    repo = MockSubscriptionRepository()
    repo._data = {}
    return repo


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
    return RedisRateLimiter(redis=FakeValkey())


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)


@pytest_asyncio.fixture
async def labour_service(
    labour_repo: LabourRepository,
) -> LabourService:
    return LabourService(
        labour_repository=labour_repo,
        event_producer=AsyncMock(),
    )


@pytest_asyncio.fixture
async def contraction_service(
    labour_repo: LabourRepository,
) -> ContractionService:
    return ContractionService(labour_repository=labour_repo)


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
    token_generator: TokenGenerator,
) -> SubscriptionService:
    return SubscriptionService(
        labour_query_service=labour_query_service,
        subscription_repository=subscription_repo,
        token_generator=token_generator,
        event_producer=AsyncMock(),
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
    subscription_authorization_service: SubscriptionAuthorizationService,
) -> SubscriptionManagementService:
    return SubscriptionManagementService(
        subscription_repository=subscription_repo,
        subscription_authorization_service=subscription_authorization_service,
        event_producer=AsyncMock(),
    )
