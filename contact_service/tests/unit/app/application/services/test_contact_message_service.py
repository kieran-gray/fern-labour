from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from src.application.contact_message_service import ContactMessageService
from src.application.dtos import ContactMessageDTO
from src.domain.enums import ContactMessageCategory
from src.domain.exceptions import InvalidContactMessageCategory
from src.domain.repository import ContactMessageRepository

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


def has_sent_email(contact_service: ContactMessageService) -> bool:
    return contact_service._event_producer.publish.call_count > 0


@pytest_asyncio.fixture
async def contact_service(contact_message_repo: ContactMessageRepository) -> ContactMessageService:
    return ContactMessageService(
        contact_message_repository=contact_message_repo,
        event_producer=AsyncMock(),
        contact_email="support@test.com",
    )


async def test_can_send_contact_email(contact_service: ContactMessageService) -> None:
    await contact_service.send_contact_email(
        email="test@email.com", name="Test User", message="Hey, I have an issue"
    )
    assert has_sent_email(contact_service=contact_service)


async def test_can_create_contact_message(contact_service: ContactMessageService) -> None:
    contact_message = await contact_service.create_message(
        category=ContactMessageCategory.ERROR_REPORT,
        email="test@email.com",
        name="Test User",
        message="Hey, I have an issue",
    )
    assert isinstance(contact_message, ContactMessageDTO)


async def test_cannot_create_contact_message_invalid_category(
    contact_service: ContactMessageService,
) -> None:
    with pytest.raises(InvalidContactMessageCategory):
        await contact_service.create_message(
            category="fail",
            email="test@email.com",
            name="Test User",
            message="Hey, I have an issue",
        )
