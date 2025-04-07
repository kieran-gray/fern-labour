import pytest_asyncio

from app.common.application.services.contact_service import ContactService
from app.notification.application.services.notification_service import NotificationService
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def has_sent_email(contact_service: ContactService) -> bool:
    email_gateway = contact_service._notification_service._email_notification_gateway
    return email_gateway.sent_notifications != []


@pytest_asyncio.fixture
async def contact_service(
    notification_service: NotificationService,
    email_template_engine: EmailTemplateEngine,
) -> ContactService:
    return ContactService(
        notification_service=notification_service,
        email_template_engine=email_template_engine,
        contact_email="support@test.com",
    )


async def test_can_send_contact_email(contact_service: ContactService) -> None:
    await contact_service.send_contact_email(
        email="test@email.com", name="Test User", message="Hey, I have an issue"
    )
    assert has_sent_email(contact_service=contact_service)
