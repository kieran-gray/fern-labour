import logging
from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.events.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.domain.base.event import DomainEvent
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.subscription.enums import ContactMethod

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event(birthing_person_id: str, labour_id: str, notes: str = "") -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="labour.completed",
        data={"birthing_person_id": birthing_person_id, "labour_id": labour_id, "notes": notes},
        time=datetime.now(UTC),
    )


def has_sent_email(event_handler: LabourCompletedEventHandler) -> bool:
    email_gateway = event_handler._notification_service._email_notification_gateway
    return email_gateway.sent_notifications != []


def has_sent_sms(event_handler: LabourCompletedEventHandler) -> bool:
    sms_gateway = event_handler._notification_service._sms_notification_gateway
    return sms_gateway.sent_notifications != []


@pytest_asyncio.fixture
async def labour_completed_event_handler(
    birthing_person_service: BirthingPersonService,
    subscriber_service: SubscriberService,
    notification_service: NotificationService,
    subscription_service: SubscriptionService,
    email_generation_service: EmailGenerationService,
) -> LabourCompletedEventHandler:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="user",
        last_name="name",
    )
    await subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="sub",
        last_name="scriber",
        phone_number="07123123123",
        email="test@subscriber.com",
    )
    return LabourCompletedEventHandler(
        birthing_person_service=birthing_person_service,
        subscriber_service=subscriber_service,
        notification_service=notification_service,
        subscription_service=subscription_service,
        email_generation_service=email_generation_service,
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


async def test_labour_completed_event_no_subscribers(
    labour_completed_event_handler: LabourCompletedEventHandler, labour: LabourDTO
) -> None:
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_non_existent_birthing_person(
    labour_completed_event_handler: LabourCompletedEventHandler,
) -> None:
    event = generate_domain_event(birthing_person_id="TEST", labour_id="TEST")
    with pytest.raises(BirthingPersonNotFoundById):
        await labour_completed_event_handler.handle(event.to_dict())


async def test_labour_completed_event_non_existent_subscriber(
    caplog: pytest.LogCaptureFixture,
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
) -> None:
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    labour_completed_event_handler._subscriber_service._subscriber_repository._data = {}

    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    module = "app.application.events.event_handlers.labour_completed_event_handler"
    with caplog.at_level(logging.ERROR, logger=module):
        await labour_completed_event_handler.handle(event.to_dict())
        assert len(caplog.records) == 1
        assert caplog.messages[0] == f"Subscriber with id '{SUBSCRIBER}' is not found."


async def test_labour_completed_event_has_subscriber_no_contact_methods(
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
) -> None:
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_email(
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    subscription = await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_completed_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_sms(
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    subscription = await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_all_contact_methods(
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    subscription = await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=BIRTHING_PERSON, labour_id=labour.id, notes="FINDME"
    )
    await labour_completed_event_handler.handle(event.to_dict())
    sent_emails = labour_completed_event_handler._notification_service._email_notification_gateway.sent_notifications
    sent_sms = labour_completed_event_handler._notification_service._sms_notification_gateway.sent_notifications
    assert sent_emails != []
    assert sent_sms != []
    assert "FINDME" in sent_emails[0].message
    assert "FINDME" in sent_sms[0].message


async def test_labour_completed_event_has_subscriber_all_contact_methods_no_phone_number_or_email(
    labour_completed_event_handler: LabourCompletedEventHandler,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    subscriber = await labour_completed_event_handler._subscriber_service.register(
        subscriber_id="new_subscriber",
        first_name="test",
        last_name="noContact",
    )
    token = labour_completed_event_handler._subscription_service._token_generator.generate(
        labour.id
    )
    subscription = await labour_completed_event_handler._subscription_service.subscribe_to(
        subscriber_id=subscriber.id, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id="new_subscriber",
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)
