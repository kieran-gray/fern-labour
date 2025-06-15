import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fern_labour_core.events.event import DomainEvent

from src.core.domain.domain_event.repository import DomainEventRepository
from src.subscription.application.event_handlers.mapping import SUBSCRIPTION_EVENT_HANDLER_MAPPING
from src.subscription.application.event_handlers.subscriber_requested_event_handler import (
    SubscriberRequestedEventHandler,
)
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId
from tests.unit.app.application.events.conftest import has_sent_email

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def generate_domain_event() -> DomainEvent:
    return DomainEvent(
        id="event_id",
        type="subscriber.approved",
        aggregate_id="just-metadata",
        aggregate_type="subscription",
        data={
            "birthing_person_id": BIRTHING_PERSON,
            "subscriber_id": SUBSCRIBER,
            "labour_id": "test-labour-id",
            "subscription_id": "just-metadata",
        },
        time=datetime.now(UTC),
    )


@pytest_asyncio.fixture
async def subscriber_requested_event_handler(
    user_service: UserQueryService,
    domain_event_repo: DomainEventRepository,
) -> SubscriberRequestedEventHandler:
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
    return SubscriberRequestedEventHandler(
        user_service=user_service,
        domain_event_repository=domain_event_repo,
        domain_event_publisher=AsyncMock(),
        tracking_link="http://localhost:5173",
    )


async def test_subscriber_requested_event_handler(
    subscriber_requested_event_handler: SubscriberRequestedEventHandler,
) -> None:
    event = generate_domain_event()
    await subscriber_requested_event_handler.handle(event.to_dict())
    assert has_sent_email(subscriber_requested_event_handler)


async def test_subscriber_requested_publish_error(
    subscriber_requested_event_handler: SubscriberRequestedEventHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    event = generate_domain_event()

    publish_mock = AsyncMock()
    publish_mock.side_effect = Exception()
    subscriber_requested_event_handler._domain_event_publisher.publish_batch = publish_mock

    with caplog.at_level(logging.ERROR):
        await subscriber_requested_event_handler.handle(event.to_dict())

    assert has_sent_email(subscriber_requested_event_handler)
    assert "Error creating background publishing job" in caplog.text


def test_mapping():
    assert (
        SUBSCRIPTION_EVENT_HANDLER_MAPPING.get("subscriber.requested")
        == SubscriberRequestedEventHandler
    )
