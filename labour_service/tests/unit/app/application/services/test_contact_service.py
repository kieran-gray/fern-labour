from unittest.mock import AsyncMock

import pytest_asyncio

from app.common.application.services.contact_service import ContactService

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def has_sent_email(contact_service: ContactService) -> bool:
    return contact_service._event_producer.publish.call_count > 0


@pytest_asyncio.fixture
async def contact_service() -> ContactService:
    return ContactService(
        event_producer=AsyncMock(),
        contact_email="support@test.com",
    )


async def test_can_send_contact_email(contact_service: ContactService) -> None:
    await contact_service.send_contact_email(
        email="test@email.com", name="Test User", message="Hey, I have an issue"
    )
    assert has_sent_email(contact_service=contact_service)
