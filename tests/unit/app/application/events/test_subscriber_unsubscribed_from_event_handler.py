from datetime import datetime

import pytest
import pytest_asyncio

from app.application.events.event_handlers.subscriber_unsubscribed_from_event_handler import (
    SubscriberUnsubscribedFromEventHandler,
)
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@pytest_asyncio.fixture
async def subscriber_unsubscribed_from_event_handler(
    birthing_person_repo: BirthingPersonRepository,
) -> SubscriberUnsubscribedFromEventHandler:
    test_birthing_person = BirthingPerson.create(
        birthing_person_id="test_birthing_person",
        first_name="user",
        last_name="name",
        first_labour=False,
    )
    test_birthing_person.subscribers.append(SubscriberId("test_subscriber"))
    await birthing_person_repo.save(test_birthing_person)
    return SubscriberUnsubscribedFromEventHandler(birthing_person_repo)


async def test_can_unsubscribe_from_birthing_person(
    subscriber_unsubscribed_from_event_handler: SubscriberUnsubscribedFromEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="subscriber.unsubscribed_from",
        data={"subscriber_id": "test_subscriber", "birthing_person_id": "test_birthing_person"},
        time=datetime.now(),
    )
    await subscriber_unsubscribed_from_event_handler.handle(event.to_dict())
    repo = subscriber_unsubscribed_from_event_handler._birthing_person_repository

    birthing_person = await repo.get_by_id(BirthingPersonId("test_birthing_person"))
    assert birthing_person.subscribers == []


async def test_cannot_unsubscribe_from_non_existent_birthing_person(
    subscriber_unsubscribed_from_event_handler: SubscriberUnsubscribedFromEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="subscriber.unsubscribed_from",
        data={
            "subscriber_id": "test_subscriber",
            "birthing_person_id": "this_birthing_person_does_not_exist",
        },
        time=datetime.now(),
    )
    with pytest.raises(BirthingPersonNotFoundById):
        await subscriber_unsubscribed_from_event_handler.handle(event.to_dict())
