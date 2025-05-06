from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest_asyncio
from fern_labour_core.events.event import DomainEvent
from fern_labour_notifications_shared.enums import NotificationChannel
from fern_labour_notifications_shared.events import NotificationRequested

from src.subscription.application.event_handlers.mapping import SUBSCRIPTION_EVENT_HANDLER_MAPPING
from src.subscription.application.event_handlers.subscriber_approved_event_handler import (
    SubscriberApprovedEventHandler,
)
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event() -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="subscriber.approved",
        data={
            "birthing_person_id": BIRTHING_PERSON,
            "subscriber_id": SUBSCRIBER,
            "labour_id": "test-labour-id",
            "subscription_id": "just-metadata",
        },
        time=datetime.now(UTC),
    )


def has_sent_email(event_handler: SubscriberApprovedEventHandler) -> bool:
    for call in event_handler._event_producer.publish.mock_calls:
        event: NotificationRequested = call.kwargs["event"]
        if event.data["channel"] == NotificationChannel.EMAIL.value:
            return True
    return False


@pytest_asyncio.fixture
async def subscriber_approved_event_handler(
    user_service: UserQueryService,
) -> SubscriberApprovedEventHandler:
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
    return SubscriberApprovedEventHandler(
        user_service=user_service,
        event_producer=AsyncMock(),
        tracking_link="http://localhost:5173",
    )


async def test_subscriber_approved_event_handler(
    subscriber_approved_event_handler: SubscriberApprovedEventHandler,
) -> None:
    event = generate_domain_event()
    await subscriber_approved_event_handler.handle(event.to_dict())
    assert has_sent_email(subscriber_approved_event_handler)


def test_mapping():
    assert (
        SUBSCRIPTION_EVENT_HANDLER_MAPPING.get("subscriber.approved")
        == SubscriberApprovedEventHandler
    )
