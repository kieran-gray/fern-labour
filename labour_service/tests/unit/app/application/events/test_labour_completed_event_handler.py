import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fern_labour_core.events.event import DomainEvent
from fern_labour_notifications_shared.notification_data import (
    LabourCompletedData,
    LabourCompletedWithNoteData,
)

from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from src.labour.application.services.labour_service import LabourService
from src.subscription.application.dtos import SubscriptionDTO
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.enums import ContactMethod, SubscriptionAccessLevel
from src.user.application.dtos.user import UserDTO
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.exceptions import UserNotFoundById
from src.user.domain.value_objects.user_id import UserId
from tests.unit.app.application.events.conftest import has_sent_email, has_sent_sms

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event(birthing_person_id: str, labour_id: str, notes: str = "") -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="labour.completed",
        aggregate_id=labour_id,
        aggregate_type="labour",
        data={"birthing_person_id": birthing_person_id, "labour_id": labour_id, "notes": notes},
        time=datetime.now(UTC),
    )


@pytest_asyncio.fixture
async def labour_completed_event_handler(
    user_service: UserQueryService,
    domain_event_repo: DomainEventRepository,
    subscription_query_service: SubscriptionQueryService,
) -> LabourCompletedEventHandler:
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
    return LabourCompletedEventHandler(
        user_service=user_service,
        domain_event_repository=domain_event_repo,
        domain_event_publisher=AsyncMock(),
        subscription_query_service=subscription_query_service,
        tracking_link="http://localhost:5173",
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


@pytest_asyncio.fixture
async def paid_subscription(
    labour: LabourDTO,
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
) -> SubscriptionDTO:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    return await subscription_management_service.update_access_level(
        subscription_id=subscription.id, access_level=SubscriptionAccessLevel.SUPPORTER
    )


@pytest_asyncio.fixture
async def basic_subscription(
    labour: LabourDTO,
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
) -> SubscriptionDTO:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    return await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
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
    with pytest.raises(UserNotFoundById):
        await labour_completed_event_handler.handle(event.to_dict())


async def test_generation_returns_correct_dataclass(
    labour_completed_event_handler: LabourCompletedEventHandler,
) -> None:
    birthing_person = UserDTO(
        id="bp_123",
        username="bptest",
        first_name="user",
        last_name="name",
        email="test@bp.com",
        phone_number=None,
    )
    subscriber = UserDTO(
        id="sub_123",
        username="subtest",
        first_name="hello",
        last_name="world",
        email="test@s.com",
        phone_number=None,
    )
    result = labour_completed_event_handler._generate_notification_data(
        birthing_person=birthing_person, subscriber=subscriber, notes=""
    )
    assert isinstance(result, LabourCompletedData)


async def test_generation_with_notes_returns_correct_dataclass(
    labour_completed_event_handler: LabourCompletedEventHandler,
) -> None:
    birthing_person = UserDTO(
        id="bp_123",
        username="bptest",
        first_name="user",
        last_name="name",
        email="test@bp.com",
        phone_number=None,
    )
    subscriber = UserDTO(
        id="sub_123",
        username="subtest",
        first_name="hello",
        last_name="world",
        email="test@s.com",
        phone_number=None,
    )
    result = labour_completed_event_handler._generate_notification_data(
        birthing_person=birthing_person, subscriber=subscriber, notes="test notes"
    )
    assert isinstance(result, LabourCompletedWithNoteData)


async def test_labour_completed_event_non_existent_subscriber(
    caplog: pytest.LogCaptureFixture,
    labour_completed_event_handler: LabourCompletedEventHandler,
    paid_subscription: SubscriptionDTO,
) -> None:
    labour_completed_event_handler._user_service._user_repository._data.pop(
        paid_subscription.subscriber_id
    )

    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    module = "src.application.events.event_handlers.labour_completed_event_handler"
    with caplog.at_level(logging.ERROR, logger=module):
        await labour_completed_event_handler.handle(event.to_dict())
        assert len(caplog.records) == 1
        assert (
            caplog.messages[0] == f"User with id '{paid_subscription.subscriber_id}' is not found."
        )


async def test_labour_completed_event_has_subscriber_no_contact_methods(
    labour_completed_event_handler: LabourCompletedEventHandler,
    paid_subscription: SubscriptionDTO,
) -> None:
    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_email(
    labour_completed_event_handler: LabourCompletedEventHandler,
    paid_subscription: SubscriptionDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await subscription_management_service.update_contact_methods(
        requester_id=paid_subscription.subscriber_id,
        subscription_id=paid_subscription.id,
        contact_methods=[ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_sms(
    labour_completed_event_handler: LabourCompletedEventHandler,
    paid_subscription: SubscriptionDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await subscription_management_service.update_contact_methods(
        requester_id=paid_subscription.subscriber_id,
        subscription_id=paid_subscription.id,
        contact_methods=[ContactMethod.SMS.value],
    )
    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_all_contact_methods(
    labour_completed_event_handler: LabourCompletedEventHandler,
    paid_subscription: SubscriptionDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await subscription_management_service.update_contact_methods(
        requester_id=paid_subscription.subscriber_id,
        subscription_id=paid_subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert has_sent_email(labour_completed_event_handler)
    assert has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_has_subscriber_all_contact_methods_no_phone_number_or_email(
    labour_completed_event_handler: LabourCompletedEventHandler,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await labour_completed_event_handler._user_service._user_repository.save(
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
    await subscription_management_service.approve_subscriber(
        requester_id=labour.birthing_person_id, subscription_id=subscription.id
    )
    await subscription_management_service.update_access_level(
        subscription_id=subscription.id,
        access_level=SubscriptionAccessLevel.SUPPORTER,
    )
    await subscription_management_service.update_contact_methods(
        requester_id="new_subscriber",
        subscription_id=subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=subscription.birthing_person_id, labour_id=subscription.labour_id
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_completed_event_basic_subscriber(
    labour_completed_event_handler: LabourCompletedEventHandler,
    basic_subscription: SubscriptionDTO,
    subscription_management_service: SubscriptionManagementService,
) -> None:
    await subscription_management_service.update_contact_methods(
        requester_id=basic_subscription.subscriber_id,
        subscription_id=basic_subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=basic_subscription.birthing_person_id,
        labour_id=basic_subscription.labour_id,
    )
    await labour_completed_event_handler.handle(event.to_dict())
    assert not has_sent_email(labour_completed_event_handler)
    assert not has_sent_sms(labour_completed_event_handler)


async def test_labour_begun_event_publish_failure(
    labour_completed_event_handler: LabourCompletedEventHandler,
    subscription_management_service: SubscriptionManagementService,
    paid_subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
) -> None:
    await subscription_management_service.update_contact_methods(
        requester_id=paid_subscription.subscriber_id,
        subscription_id=paid_subscription.id,
        contact_methods=[ContactMethod.SMS.value, ContactMethod.EMAIL.value],
    )
    event = generate_domain_event(
        birthing_person_id=paid_subscription.birthing_person_id,
        labour_id=paid_subscription.labour_id,
    )
    publish_mock = AsyncMock()
    publish_mock.side_effect = Exception()

    labour_completed_event_handler._domain_event_publisher.publish_batch = publish_mock

    with caplog.at_level(logging.ERROR):
        await labour_completed_event_handler.handle(event.to_dict())

    assert has_sent_email(labour_completed_event_handler)
    assert has_sent_sms(labour_completed_event_handler)
    assert "Error creating background publishing job" in caplog.text
