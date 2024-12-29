from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.events.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.exceptions import SubscriberNotFoundById
from app.domain.subscriber.vo_subscriber_id import SubscriberId

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


@pytest_asyncio.fixture
async def labour_begun_event_handler(
    birthing_person_service: BirthingPersonService,
    subscriber_service: SubscriberService,
    notification_service: NotificationService,
) -> LabourBegunEventHandler:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="user",
        last_name="name",
    )
    return LabourBegunEventHandler(
        birthing_person_service=birthing_person_service,
        subscriber_service=subscriber_service,
        notification_service=notification_service,
    )


async def add_subscriber_to_birthing_person(
    birthing_person_service: BirthingPersonService, birthing_person_id: str, subscriber_id: str
) -> None:
    birthing_person_repo = birthing_person_service._birthing_person_repository
    birthing_person = await birthing_person_repo.get_by_id(BirthingPersonId(birthing_person_id))
    birthing_person.subscribers.append(SubscriberId(subscriber_id))
    await birthing_person_repo.save(birthing_person)


async def test_labour_begun_event_no_subscribers(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        == []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        == []
    )


async def test_labour_begun_event_non_existent_birthing_person(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": "TEST"},
        time=datetime.now(UTC),
    )
    with pytest.raises(BirthingPersonNotFoundById):
        await labour_begun_event_handler.handle(event.to_dict())


async def test_labour_begun_event_non_existent_subscriber(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id="TEST",
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    with pytest.raises(SubscriberNotFoundById):
        await labour_begun_event_handler.handle(event.to_dict())


async def test_labour_begun_event_has_subscriber_no_contact_methods(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await labour_begun_event_handler._subscriber_service.register(
        subscriber_id=SUBSCRIBER, first_name="test", last_name="test", contact_methods=[]
    )
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id=SUBSCRIBER,
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        == []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        == []
    )


async def test_labour_begun_event_has_subscriber_email(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await labour_begun_event_handler._subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="test",
        contact_methods=["email"],
        email="test@email.com",
    )
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id=SUBSCRIBER,
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        != []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        == []
    )


async def test_labour_begun_event_has_subscriber_sms(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await labour_begun_event_handler._subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="test",
        contact_methods=["sms"],
        phone_number="07123123123",
    )
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id=SUBSCRIBER,
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        == []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        != []
    )


async def test_labour_begun_event_has_subscriber_all_contact_methods(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await labour_begun_event_handler._subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="test",
        contact_methods=["sms", "email"],
        email="test@email.com",
        phone_number="07123123123",
    )
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id=SUBSCRIBER,
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        != []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        != []
    )


async def test_labour_begun_event_has_subscriber_all_contact_methods_no_phone_number_or_email(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    await labour_begun_event_handler._subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="test",
        contact_methods=["sms", "email"],
    )
    await add_subscriber_to_birthing_person(
        birthing_person_service=labour_begun_event_handler._birthing_person_service,
        birthing_person_id=BIRTHING_PERSON,
        subscriber_id=SUBSCRIBER,
    )

    event = DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    await labour_begun_event_handler.handle(event.to_dict())
    assert (
        labour_begun_event_handler._notification_service._email_notification_gateway.sent_notifications
        == []
    )
    assert (
        labour_begun_event_handler._notification_service._sms_notification_gateway.sent_notifications
        == []
    )
