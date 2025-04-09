import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.common.domain.event import DomainEvent
from app.labour.application.dtos.labour import LabourDTO
from app.labour.application.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.application.services.subscription_service import SubscriptionService
from app.subscription.domain.enums import ContactMethod
from app.user.application.services.user_service import UserService
from app.user.domain.entity import User
from app.user.domain.exceptions import UserNotFoundById
from app.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event(birthing_person_id: str, labour_id: str) -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="labour.begun",
        data={"birthing_person_id": birthing_person_id, "labour_id": labour_id},
        time=datetime.now(UTC),
    )


def has_sent_email(event_handler: LabourBegunEventHandler) -> bool:
    return event_handler._event_producer.publish.call_count > 0


def has_sent_sms(event_handler: LabourBegunEventHandler) -> bool:
    return event_handler._event_producer.publish.call_count > 0


@pytest_asyncio.fixture
async def labour_begun_event_handler(
    user_service: UserService,
    subscription_query_service: SubscriptionQueryService,
) -> LabourBegunEventHandler:
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
    return LabourBegunEventHandler(
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


async def test_labour_begun_event_no_subscribers(
    labour_begun_event_handler: LabourBegunEventHandler, labour: LabourDTO
) -> None:
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_begun_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_begun_event_handler)
    assert not has_sent_sms(labour_begun_event_handler)


async def test_labour_begun_event_non_existent_birthing_person(
    labour_begun_event_handler: LabourBegunEventHandler,
) -> None:
    event = generate_domain_event(birthing_person_id="TEST", labour_id="TEST")
    with pytest.raises(UserNotFoundById):
        await labour_begun_event_handler.handle(event.to_dict())


async def test_labour_begun_event_non_existent_subscriber(
    caplog: pytest.LogCaptureFixture,
    labour_begun_event_handler: LabourBegunEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    labour_begun_event_handler._user_service._user_repository._data.pop(SUBSCRIBER)
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    module = "app.application.events.event_handlers.labour_begun_event_handler"
    with caplog.at_level(logging.ERROR, logger=module):
        await labour_begun_event_handler.handle(event.to_dict())
        assert len(caplog.records) == 1
        assert caplog.messages[0] == f"User with id '{SUBSCRIBER}' is not found."


async def test_labour_begun_event_has_subscriber_no_contact_methods(
    labour_begun_event_handler: LabourBegunEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_begun_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_begun_event_handler)
    assert not has_sent_sms(labour_begun_event_handler)


async def test_labour_begun_event_has_subscriber_email(
    labour_begun_event_handler: LabourBegunEventHandler,
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
    await labour_begun_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_begun_event_handler)
    assert not has_sent_sms(labour_begun_event_handler)


async def test_labour_begun_event_has_subscriber_sms(
    labour_begun_event_handler: LabourBegunEventHandler,
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
    await labour_begun_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_begun_event_handler)
    assert has_sent_sms(labour_begun_event_handler)


async def test_labour_begun_event_has_subscriber_all_contact_methods(
    labour_begun_event_handler: LabourBegunEventHandler,
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
    event = generate_domain_event(birthing_person_id=BIRTHING_PERSON, labour_id=labour.id)
    await labour_begun_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_begun_event_handler)
    assert has_sent_sms(labour_begun_event_handler)


async def test_labour_begun_event_has_subscriber_all_contact_methods_no_phone_number_or_email(
    labour_begun_event_handler: LabourBegunEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await labour_begun_event_handler._user_service._user_repository.save(
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
    await labour_begun_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_begun_event_handler)
    assert not has_sent_sms(labour_begun_event_handler)
