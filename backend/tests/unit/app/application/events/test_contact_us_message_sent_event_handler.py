from datetime import UTC, datetime

import pytest_asyncio

from app.application.events.event_handlers.contact_us_message_sent_event_handler import (
    ContactUsMessageSentEventHandler,
)
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.domain.base.event import DomainEvent

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def has_sent_email(event_handler: ContactUsMessageSentEventHandler) -> bool:
    email_gateway = event_handler._notification_service._email_notification_gateway
    return email_gateway.sent_notifications != []


@pytest_asyncio.fixture
async def contact_us_message_sent_event_handler(
    notification_service: NotificationService,
    email_generation_service: EmailGenerationService,
) -> ContactUsMessageSentEventHandler:
    return ContactUsMessageSentEventHandler(
        notification_service=notification_service,
        email_generation_service=email_generation_service,
        contact_email="support@test.com",
    )


async def test_generate_contact_us_message(
    contact_us_message_sent_event_handler: ContactUsMessageSentEventHandler,
) -> None:
    event = DomainEvent(
        id="event_id",
        type="contact-us.message-sent",
        data={"email": "test@email.com", "user_id": "", "data": "test contact message"},
        time=datetime.now(UTC),
    )
    await contact_us_message_sent_event_handler.handle(event.to_dict())
    assert has_sent_email(contact_us_message_sent_event_handler)
