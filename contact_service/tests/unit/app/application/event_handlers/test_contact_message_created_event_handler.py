from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest_asyncio
from fern_labour_core.events.event import DomainEvent
from fern_labour_notifications_shared.enums import NotificationChannel
from fern_labour_notifications_shared.events import NotificationRequested

from src.application.contact_message_query_service import ContactMessageQueryService
from src.application.contact_message_service import ContactMessageService
from src.application.event_handlers.contact_message_created_event_handler import (
    ContactMessageCreatedEventHandler,
)
from src.application.event_handlers.mapping import CONTACT_EVENT_HANDLER_MAPPING
from src.domain.enums import ContactMessageCategory

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


@pytest_asyncio.fixture
async def domain_event(contact_message_service: ContactMessageService) -> DomainEvent:
    message = await contact_message_service.create_message(
        category=ContactMessageCategory.ERROR_REPORT,
        email="test@email.com",
        name="Test User",
        message="Hey, I have an issue",
    )
    return DomainEvent(
        id="event_id",
        type="contact-message.created",
        data={"contact_message_id": message.id},
        time=datetime.now(UTC),
    )


def has_sent_email(event_handler: ContactMessageCreatedEventHandler) -> bool:
    for call in event_handler._event_producer.publish.mock_calls:
        event: NotificationRequested = call.kwargs["event"]
        if event.data["channel"] == NotificationChannel.EMAIL.value:
            return True
    return False


@pytest_asyncio.fixture
async def contact_message_created_event_handler(
    contact_message_query_service: ContactMessageQueryService,
) -> ContactMessageCreatedEventHandler:
    return ContactMessageCreatedEventHandler(
        contact_message_query_service=contact_message_query_service,
        event_producer=AsyncMock(),
        contact_email="support@test.com",
    )


async def test_contact_message_created_event_handler(
    contact_message_created_event_handler: ContactMessageCreatedEventHandler,
    domain_event: DomainEvent,
) -> None:
    await contact_message_created_event_handler.handle(domain_event.to_dict())
    assert has_sent_email(contact_message_created_event_handler)


def test_mapping():
    assert (
        CONTACT_EVENT_HANDLER_MAPPING.get("contact-message.created")
        == ContactMessageCreatedEventHandler
    )
