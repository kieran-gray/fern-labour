import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.domain.labour.entity import Labour
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.vo_subscription_id import SubscriptionId
from app.domain.user.entity import User
from app.domain.user.repository import UserRepository
from app.domain.user.vo_user_id import UserId


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

    async def save(self, labour_id: Labour) -> None:
        self._data[labour_id.id_.value] = labour_id

    async def delete(self, labour_id: Labour) -> None:
        self._data.pop(labour_id.id_.value)

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
            subscriptions.append(subscription)
        return subscriptions

    async def filter_one_or_none(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: UserId | None = None,
        birthing_person_id: UserId | None = None,
        subscription_status: SubscriptionStatus | None = None,
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


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: dict[str, Any]) -> None:
        self.sent_notifications.append(data)


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: dict[str, Any]) -> None:
        self.sent_notifications.append(data)


class MockEmailGenerationService(EmailGenerationService):
    directory = Path()

    def generate(self, template_name: str, data: dict[str, Any]) -> str:
        return f"Mock HTML email: {template_name} {json.dumps(data)}"


@pytest.fixture
def token_generator() -> TokenGenerator:
    return MockTokenGenerator()


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserService:
    return UserService(user_repository=user_repo)


@pytest_asyncio.fixture
async def labour_service(
    user_service: UserService,
    labour_repo: LabourRepository,
) -> LabourService:
    return LabourService(
        user_service=user_service,
        labour_repository=labour_repo,
        event_producer=AsyncMock(),
    )


@pytest_asyncio.fixture
async def get_labour_service(
    labour_repo: LabourRepository,
) -> GetLabourService:
    return GetLabourService(
        labour_repository=labour_repo,
    )


@pytest_asyncio.fixture
async def subscription_service(
    get_labour_service: GetLabourService,
    user_service: UserService,
    subscription_repo: SubscriptionRepository,
    token_generator: TokenGenerator,
) -> SubscriptionService:
    return SubscriptionService(
        get_labour_service=get_labour_service,
        user_service=user_service,
        subscription_repository=subscription_repo,
        token_generator=token_generator,
        event_producer=AsyncMock(),
    )


@pytest_asyncio.fixture
async def subscription_management_service(
    subscription_repo: SubscriptionRepository,
) -> SubscriptionManagementService:
    return SubscriptionManagementService(
        subscription_repository=subscription_repo, event_producer=AsyncMock()
    )


@pytest_asyncio.fixture
async def notification_service() -> NotificationService:
    email_notification_gateway = MockEmailNotificationGateway()
    sms_notification_gateway = MockSMSNotificationGateway()
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    return NotificationService(
        email_notification_gateway=email_notification_gateway,
        sms_notification_gateway=sms_notification_gateway,
    )


@pytest_asyncio.fixture
async def email_generation_service() -> EmailGenerationService:
    return MockEmailGenerationService()
