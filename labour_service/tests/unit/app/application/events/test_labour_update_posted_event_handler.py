import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from src.common.domain.event import DomainEvent
from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.enums import LabourPaymentPlan
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.notification.enums import NotificationType
from src.notification.events import NotificationRequested
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.enums import ContactMethod
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.exceptions import UserNotFoundById
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event(
    birthing_person_id: str,
    labour_id: str,
    message: str = "test message",
    update_type: LabourUpdateType = LabourUpdateType.ANNOUNCEMENT,
) -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="labour.update-posted",
        data={
            "birthing_person_id": birthing_person_id,
            "labour_id": labour_id,
            "labour_update_id": str(uuid4()),
            "message": message,
            "labour_update_type": update_type,
        },
        time=datetime.now(UTC),
    )


@pytest_asyncio.fixture
async def labour_update_posted_event_handler(
    user_service: UserQueryService,
    subscription_query_service: SubscriptionQueryService,
) -> LabourUpdatePostedEventHandler:
    await user_service._user_repository.save(
        User(
            id_=UserId(BIRTHING_PERSON),
            username="test789",
            first_name="user",
            last_name="name",
            email="test@birthing.com",
        )
    )
    await user_service._user_repository.save(
        User(
            id_=UserId(SUBSCRIBER),
            username="test456",
            first_name="sub",
            last_name="scriber",
            email="test@subscriber.com",
            phone_number="07123123123",
        )
    )
    return LabourUpdatePostedEventHandler(
        user_service=user_service,
        event_producer=AsyncMock(),
        subscription_query_service=subscription_query_service,
        tracking_link="http://localhost:5173",
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    return await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY.value
    )


def has_sent_email(event_handler: LabourUpdatePostedEventHandler) -> bool:
    for call in event_handler._event_producer.publish.mock_calls:
        event: NotificationRequested = call.kwargs["event"]
        if event.data["type"] == NotificationType.EMAIL.value:
            return True
    return False


def has_sent_sms(event_handler: LabourUpdatePostedEventHandler) -> bool:
    for call in event_handler._event_producer.publish.mock_calls:
        event: NotificationRequested = call.kwargs["event"]
        if event.data["type"] == NotificationType.SMS.value:
            return True
    return False


async def test_labour_update_posted_event_no_subscribers(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler, labour: LabourDTO
) -> None:
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_update_posted_event_handler)
    assert not has_sent_sms(labour_update_posted_event_handler)


async def test_labour_update_posted_event_non_existent_birthing_person(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
) -> None:
    event = generate_domain_event(birthing_person_id="TEST", labour_id="TEST")
    with pytest.raises(UserNotFoundById):
        await labour_update_posted_event_handler.handle(event.to_dict())


async def test_labour_update_posted_event_non_existent_subscriber(
    caplog: pytest.LogCaptureFixture,
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    labour_update_posted_event_handler._user_service._user_repository._data.pop(SUBSCRIBER)

    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)

    module = "src.application.events.event_handlers.labour_update_posted_event_handler"
    with caplog.at_level(logging.ERROR, logger=module):
        await labour_update_posted_event_handler.handle(event.to_dict())
        assert len(caplog.records) == 1
        assert caplog.messages[0] == f"User with id '{SUBSCRIBER}' is not found."


async def test_labour_update_posted_event_has_subscriber_no_contact_methods(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_update_posted_event_handler)
    assert not has_sent_sms(labour_update_posted_event_handler)


async def test_labour_update_posted_event_has_subscriber_email(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_update_posted_event_handler)
    assert not has_sent_sms(labour_update_posted_event_handler)


async def test_labour_update_posted_event_has_subscriber_sms(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_update_posted_event_handler)
    assert has_sent_sms(labour_update_posted_event_handler)


async def test_labour_update_posted_event_has_subscriber_all_contact_methods(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=BIRTHING_PERSON, labour_id=labour.id, message="FINDME"
    )
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert has_sent_sms(labour_update_posted_event_handler)
    assert has_sent_email(labour_update_posted_event_handler)


async def test_labour_update_posted_event_has_subscriber_all_contact_methods_status_update(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=BIRTHING_PERSON,
        labour_id=labour.id,
        message="FINDME",
        update_type=LabourUpdateType.STATUS_UPDATE,
    )
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_update_posted_event_handler)
    assert not has_sent_sms(labour_update_posted_event_handler)


async def test_labour_update_posted_event_has_subscriber_all_contact_mthds_no_phone_number_or_email(
    labour_update_posted_event_handler: LabourUpdatePostedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await labour_update_posted_event_handler._user_service._user_repository.save(
        User(
            id_=UserId("new_subscriber"),
            username="test123",
            first_name="test",
            last_name="noContact",
            email="",
        )
    )
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id="new_subscriber", labour_id=labour.id, token=token
    )
    await subscription_management_service.update_contact_methods(
        requester_id="new_subscriber",
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_update_posted_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_update_posted_event_handler)
    assert not has_sent_sms(labour_update_posted_event_handler)
