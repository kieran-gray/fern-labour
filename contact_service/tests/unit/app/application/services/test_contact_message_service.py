import pytest

from src.application.contact_message_service import ContactMessageService
from src.application.dtos import ContactMessageDTO
from src.domain.enums import ContactMessageCategory
from src.domain.exceptions import InvalidContactMessageCategory

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


async def test_can_create_contact_message(contact_message_service: ContactMessageService) -> None:
    contact_message = await contact_message_service.create_message(
        category=ContactMessageCategory.ERROR_REPORT,
        email="test@email.com",
        name="Test User",
        message="Hey, I have an issue",
    )
    assert isinstance(contact_message, ContactMessageDTO)


async def test_cannot_create_contact_message_invalid_category(
    contact_message_service: ContactMessageService,
) -> None:
    with pytest.raises(InvalidContactMessageCategory):
        await contact_message_service.create_message(
            category="fail",
            email="test@email.com",
            name="Test User",
            message="Hey, I have an issue",
        )
