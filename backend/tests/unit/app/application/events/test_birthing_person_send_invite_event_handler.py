from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.events.event_handlers.birthing_person_send_invite_event_handler import (
    BirthingPersonSendInviteEventHandler,
)
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.exceptions import SubscriberAlreadySubscribedToBirthingPerson
from app.domain.subscriber.vo_subscriber_id import SubscriberId

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"


@pytest_asyncio.fixture
async def birthing_person_send_invite_event_handler(
    birthing_person_service: BirthingPersonService,
    notification_service: NotificationService,
    subscriber_service: SubscriberService,
    email_generation_service: EmailGenerationService,
    token_generator: TokenGenerator,
) -> BirthingPersonSendInviteEventHandler:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="user",
        last_name="name",
    )
    await subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="user",
        email="test@email.com",
        contact_methods=[],
    )
    return BirthingPersonSendInviteEventHandler(
        birthing_person_service=birthing_person_service,
        notification_service=notification_service,
        subscriber_service=subscriber_service,
        email_generation_service=email_generation_service,
        token_generator=token_generator,
    )


async def test_can_send_invite(
    birthing_person_send_invite_event_handler: BirthingPersonSendInviteEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.send-invite",
        data={"invite_email": "test@email.com", "birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    notification_service = birthing_person_send_invite_event_handler._notification_service

    assert notification_service._email_notification_gateway.sent_notifications == []
    await birthing_person_send_invite_event_handler.handle(event.to_dict())
    assert notification_service._email_notification_gateway.sent_notifications != []


async def test_cannnot_send_invite_for_non_existent_birthing_person(
    birthing_person_send_invite_event_handler: BirthingPersonSendInviteEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.send-invite",
        data={"invite_email": "test@email.com", "birthing_person_id": "fake"},
        time=datetime.now(UTC),
    )
    with pytest.raises(BirthingPersonNotFoundById):
        await birthing_person_send_invite_event_handler.handle(event.to_dict())


async def test_cannnot_send_invite_for_email_already_subscribed(
    birthing_person_send_invite_event_handler: BirthingPersonSendInviteEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="birthing-person.send-invite",
        data={"invite_email": "test@email.com", "birthing_person_id": BIRTHING_PERSON},
        time=datetime.now(UTC),
    )
    birthing_person_service = birthing_person_send_invite_event_handler._birthing_person_service
    birthing_person_repo = birthing_person_service._birthing_person_repository
    birthing_person = await birthing_person_repo.get_by_id(BirthingPersonId(BIRTHING_PERSON))
    birthing_person.add_subscriber(SubscriberId(SUBSCRIBER))
    await birthing_person_repo.save(birthing_person)

    subscriber_service = birthing_person_send_invite_event_handler._subscriber_service
    subscriber_repo = subscriber_service._subscriber_repository
    subscriber = await subscriber_repo.get_by_id(SubscriberId(SUBSCRIBER))
    subscriber.subscribe_to(BirthingPersonId(BIRTHING_PERSON))
    await subscriber_repo.save(subscriber)

    # TODO the above indicates some poor architecting

    with pytest.raises(SubscriberAlreadySubscribedToBirthingPerson):
        await birthing_person_send_invite_event_handler.handle(event.to_dict())
