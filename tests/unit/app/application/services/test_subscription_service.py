from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.subscription_service import SubscriptionService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import (
    SubscriberAlreadySubscribedToBirthingPerson,
    SubscriberNotFoundById,
    SubscriberNotSubscribedToBirthingPerson,
    SubscriptionTokenIncorrect,
)
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from tests.unit.app.application.conftest import (
    MockBirthingPersonRepository,
    MockSubscriberRepository,
)

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


class MockTokenGenerator(TokenGenerator):
    def generate(self, input: str) -> str:
        return input

    def validate(self, id: str, token: str):
        return token == id


@pytest_asyncio.fixture
def event_producer():
    return AsyncMock()


@pytest.fixture
def token_generator():
    return MockTokenGenerator()


@pytest_asyncio.fixture
async def birthing_person_repo():
    repo = MockBirthingPersonRepository()
    repo._data = {
        BIRTHING_PERSON: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON),
            first_name="Name",
            last_name="User",
            labours=[],
        )
    }
    return repo


@pytest_asyncio.fixture
async def subscriber_repo():
    repo = MockSubscriberRepository()
    repo._data = {
        SUBSCRIBER: Subscriber(
            id_=SubscriberId(SUBSCRIBER),
            first_name="First",
            last_name="Last",
            phone_number="07123123123",
            email="test@email.com",
            contact_methods=[],
        )
    }
    return repo


@pytest_asyncio.fixture
async def subscription_service(
    birthing_person_repo: BirthingPersonRepository,
    subscriber_repo: SubscriberRepository,
    event_producer: EventProducer,
    token_generator: TokenGenerator,
) -> SubscriptionService:
    return SubscriptionService(
        birthing_person_repository=birthing_person_repo,
        subscriber_repository=subscriber_repo,
        token_generator=token_generator,
        event_producer=event_producer,
    )


async def test_can_subscribe_to_birthing_person(subscription_service: SubscriptionService) -> None:
    subscriber = await subscription_service._subscriber_repository.get_by_id(
        SubscriberId(SUBSCRIBER)
    )
    assert subscriber.subscribed_to == []

    subscriber = await subscription_service.subscribe_to(
        SUBSCRIBER, BIRTHING_PERSON, BIRTHING_PERSON
    )
    assert subscriber.subscribed_to == [BIRTHING_PERSON]


async def test_cannot_subscribe_to_birthing_person_more_than_once(
    subscription_service: SubscriptionService,
) -> None:
    subscriber = await subscription_service.subscribe_to(
        SUBSCRIBER, BIRTHING_PERSON, BIRTHING_PERSON
    )
    assert subscriber.subscribed_to == [BIRTHING_PERSON]

    with pytest.raises(SubscriberAlreadySubscribedToBirthingPerson):
        await subscription_service.subscribe_to(SUBSCRIBER, BIRTHING_PERSON, BIRTHING_PERSON)


async def test_cannot_subscribe_to_non_existent_birthing_person(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(BirthingPersonNotFoundById):
        await subscription_service.subscribe_to(SUBSCRIBER, "TEST", BIRTHING_PERSON)


async def test_cannot_subscribe_with_non_existent_subscriber(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriberNotFoundById):
        await subscription_service.subscribe_to("TEST", BIRTHING_PERSON, BIRTHING_PERSON)


async def test_cannot_subscribe_to_with_incorrect_token(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriptionTokenIncorrect):
        await subscription_service.subscribe_to(SUBSCRIBER, BIRTHING_PERSON, "INVALID")


async def test_can_unsubscribe_from_birthing_person(
    subscription_service: SubscriptionService,
) -> None:
    subscriber = await subscription_service.subscribe_to(
        SUBSCRIBER, BIRTHING_PERSON, BIRTHING_PERSON
    )
    assert subscriber.subscribed_to == [BIRTHING_PERSON]

    subscriber = await subscription_service.unsubscribe_from(SUBSCRIBER, BIRTHING_PERSON)
    assert subscriber.subscribed_to == []


async def test_cannot_unsubscribed_from_birthing_person_not_subscribed_to(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriberNotSubscribedToBirthingPerson):
        await subscription_service.unsubscribe_from(SUBSCRIBER, BIRTHING_PERSON)


async def test_cannot_unsubscribe_with_non_existent_subscriber(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriberNotFoundById):
        await subscription_service.unsubscribe_from("TEST", BIRTHING_PERSON)
