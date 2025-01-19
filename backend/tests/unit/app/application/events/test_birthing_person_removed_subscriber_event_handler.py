from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.events.event_handlers.birthing_person_removed_subscriber_event_handler import (
    BirthingPersonRemovedSubscriberEventHandler,
)
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import (
    SubscriberNotFoundById,
    SubscriberNotSubscribedToBirthingPerson,
)
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@pytest_asyncio.fixture
async def birthing_person_removed_subscriber_event_handler(
    subscriber_repo: SubscriberRepository,
) -> BirthingPersonRemovedSubscriberEventHandler:
    test_subscriber: Subscriber = Subscriber.create(
        id="test_subscriber",
        first_name="user",
        last_name="name",
        contact_methods=[],
    )
    test_subscriber.subscribe_to(BirthingPersonId("test_birthing_person"))
    await subscriber_repo.save(test_subscriber)
    return BirthingPersonRemovedSubscriberEventHandler(subscriber_repo)


async def test_can_remove_subscriber(
    birthing_person_removed_subscriber_event_handler: BirthingPersonRemovedSubscriberEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.removed-subscriber",
        data={"subscriber_id": "test_subscriber", "birthing_person_id": "test_birthing_person"},
        time=datetime.now(UTC),
    )
    await birthing_person_removed_subscriber_event_handler.handle(event.to_dict())
    repo = birthing_person_removed_subscriber_event_handler._subscriber_repository

    subscriber = await repo.get_by_id(SubscriberId("test_subscriber"))
    assert subscriber.subscribed_to == []


async def test_cannot_remove_non_existent_subscriber(
    birthing_person_removed_subscriber_event_handler: BirthingPersonRemovedSubscriberEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.removed-subscriber",
        data={
            "subscriber_id": "this_subscriber_does_not_exist",
            "birthing_person_id": "test_birthing_person",
        },
        time=datetime.now(UTC),
    )
    with pytest.raises(SubscriberNotFoundById):
        await birthing_person_removed_subscriber_event_handler.handle(event.to_dict())


async def test_cannot_remove_birthing_person_for_subscriber_not_subscribed(
    birthing_person_removed_subscriber_event_handler: BirthingPersonRemovedSubscriberEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.removed-subscriber",
        data={
            "subscriber_id": "test_subscriber",
            "birthing_person_id": "this_birthing_person_does_not_exist",
        },
        time=datetime.now(UTC),
    )
    with pytest.raises(SubscriberNotSubscribedToBirthingPerson):
        await birthing_person_removed_subscriber_event_handler.handle(event.to_dict())
