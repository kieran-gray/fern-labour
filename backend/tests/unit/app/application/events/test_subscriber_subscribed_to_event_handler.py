from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.events.event_handlers.subscriber_subscribed_to_event_handler import (
    SubscriberSubscribedToEventHandler,
)
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@pytest_asyncio.fixture
async def subscriber_subscribed_to_event_handler(
    birthing_person_repo: BirthingPersonRepository,
) -> SubscriberSubscribedToEventHandler:
    test_birthing_person = BirthingPerson.create(
        birthing_person_id="test_birthing_person",
        first_name="user",
        last_name="name",
    )
    await birthing_person_repo.save(test_birthing_person)
    return SubscriberSubscribedToEventHandler(birthing_person_repo)


async def test_can_subscribe_to_birthing_person(
    subscriber_subscribed_to_event_handler: SubscriberSubscribedToEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="subscriber.subscribed_to",
        data={"subscriber_id": "test_subscriber", "birthing_person_id": "test_birthing_person"},
        time=datetime.now(UTC),
    )
    await subscriber_subscribed_to_event_handler.handle(event.to_dict())
    repo = subscriber_subscribed_to_event_handler._birthing_person_repository

    birthing_person = await repo.get_by_id(BirthingPersonId("test_birthing_person"))
    assert birthing_person.subscribers == [SubscriberId("test_subscriber")]


async def test_cannot_subscribe_to_non_existent_birthing_person(
    subscriber_subscribed_to_event_handler: SubscriberSubscribedToEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="subscriber.subscribed_to",
        data={
            "subscriber_id": "test_subscriber",
            "birthing_person_id": "this_birthing_person_does_not_exist",
        },
        time=datetime.now(UTC),
    )
    with pytest.raises(BirthingPersonNotFoundById):
        await subscriber_subscribed_to_event_handler.handle(event.to_dict())
