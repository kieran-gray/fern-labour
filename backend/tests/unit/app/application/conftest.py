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
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.vo_subscription_id import SubscriptionId


class MockBirthingPersonRepository(BirthingPersonRepository):
    _data = {}

    async def save(self, birthing_person: BirthingPerson) -> None:
        self._data[birthing_person.id_.value] = birthing_person

    async def delete(self, birthing_person: BirthingPerson) -> None:
        self._data.pop(birthing_person.id_.value)

    async def get_by_id(self, birthing_person_id: BirthingPersonId) -> BirthingPerson | None:
        return self._data.get(birthing_person_id.value, None)

    async def get_by_ids(self, birthing_person_ids: list[BirthingPersonId]) -> list[BirthingPerson]:
        birthing_persons = []
        for birthing_person_id in birthing_person_ids:
            if birthing_person := self._data.get(birthing_person_id.value, None):
                birthing_persons.append(birthing_person)
        return birthing_persons


class MockLabourRepository(LabourRepository):
    _data = {}

    async def save(self, labour_id: Labour) -> None:
        self._data[labour_id.id_.value] = labour_id

    async def delete(self, labour_id: Labour) -> None:
        self._data.pop(labour_id.id_.value)

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        return self._data.get(labour_id.value, None)

    async def get_active_labour_by_birthing_person_id(self, birthing_person_id: BirthingPersonId):
        return next(
            (
                labour
                for labour in self._data.values()
                if labour.birthing_person_id == birthing_person_id
            ),
            None,
        )


class MockSubscriberRepository(SubscriberRepository):
    _data = {}

    async def save(self, subscriber: Subscriber) -> None:
        self._data[subscriber.id_.value] = subscriber

    async def delete(self, subscriber: Subscriber) -> None:
        self._data.pop(subscriber.id_.value)

    async def get_by_id(self, subscriber_id: SubscriberId) -> Subscriber | None:
        return self._data.get(subscriber_id.value, None)

    async def get_by_ids(self, subscriber_ids: list[SubscriberId]) -> list[Subscriber]:
        subscribers = []
        for subscriber_id in subscriber_ids:
            if subscriber := self._data.get(subscriber_id.value, None):
                subscribers.append(subscriber)
        return subscribers


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
        subscriber_id: SubscriberId | None = None,
        birthing_person_id: BirthingPersonId | None = None,
    ) -> list[Subscription]:
        subscriptions = []
        for subscription in self._data.values():
            if labour_id and subscription.labour_id != labour_id:
                continue
            if subscriber_id and subscription.subscriber_id != subscriber_id:
                continue
            if birthing_person_id and subscription.birthing_person_id != birthing_person_id:
                continue
            subscriptions.append(subscription)
        return subscriptions

    async def filter_one_or_none(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: SubscriberId | None = None,
        birthing_person_id: BirthingPersonId | None = None,
    ) -> Subscription | None:
        found_subscription = None
        for subscription in self._data.values():
            if labour_id and subscription.labour_id != labour_id:
                continue
            if subscriber_id and subscription.subscriber_id != subscriber_id:
                continue
            if birthing_person_id and subscription.birthing_person_id != birthing_person_id:
                continue
            if found_subscription:
                raise ValueError("Multiple results found")
            found_subscription = subscription
        return found_subscription


@pytest_asyncio.fixture
async def birthing_person_repo() -> BirthingPersonRepository:
    repo = MockBirthingPersonRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def subscriber_repo() -> SubscriberRepository:
    repo = MockSubscriberRepository()
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
async def birthing_person_service(
    birthing_person_repo: BirthingPersonRepository,
) -> BirthingPersonService:
    return BirthingPersonService(
        birthing_person_repository=birthing_person_repo, event_producer=AsyncMock()
    )


@pytest_asyncio.fixture
async def subscriber_service(
    subscriber_repo: SubscriberRepository, token_generator: TokenGenerator
) -> SubscriberService:
    return SubscriberService(
        subscriber_repository=subscriber_repo,
        token_generator=token_generator,
    )


@pytest_asyncio.fixture
async def labour_service(
    birthing_person_service: BirthingPersonService,
    labour_repo: LabourRepository,
) -> LabourService:
    return LabourService(
        birthing_person_service=birthing_person_service,
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
    subscriber_service: SubscriberService,
    subscription_repo: SubscriptionRepository,
    token_generator: TokenGenerator,
) -> SubscriptionService:
    return SubscriptionService(
        get_labour_service=get_labour_service,
        subscriber_service=subscriber_service,
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
