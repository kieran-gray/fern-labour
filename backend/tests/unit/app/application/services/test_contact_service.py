from typing import Any
import pytest_asyncio

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.services.contact_service import ContactService

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def has_sent_email(contact_service: ContactService) -> bool:
    email_gateway = contact_service._notification_service._email_notification_gateway
    return email_gateway.sent_notifications != []


@pytest_asyncio.fixture
async def contact_service(
    notification_service: NotificationService,
    email_generation_service: EmailGenerationService,
) -> ContactService:
    return ContactService(
        notification_service=notification_service,
        email_generation_service=email_generation_service,
        contact_email="support@test.com"
    )


async def test_can_send_contact_email(contact_service: ContactService) -> None:
    await contact_service.send_contact_email(
        email="test@email.com", name="Test User", message="Hey, I have an issue"
    )
    assert has_sent_email(contact_service=contact_service)
