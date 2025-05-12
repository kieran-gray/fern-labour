from uuid import uuid4

import pytest
import pytest_asyncio

from src.application.contact_message_query_service import ContactMessageQueryService
from src.application.contact_message_service import ContactMessageService
from src.application.dtos import ContactMessageDTO
from src.domain.enums import ContactMessageCategory
from src.domain.exceptions import ContactMessageNotFoundById, InvalidContactMessageId

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


@pytest_asyncio.fixture
async def contact_message(contact_message_service: ContactMessageService) -> ContactMessageDTO:
    return await contact_message_service.create_message(
        category=ContactMessageCategory.ERROR_REPORT,
        email="test@email.com",
        name="Test User",
        message="Hey, I have an issue",
    )


async def test_can_get_contact_message(
    contact_message_query_service: ContactMessageQueryService, contact_message: ContactMessageDTO
) -> None:
    contact_message = await contact_message_query_service.get_message(
        contact_message_id=contact_message.id
    )
    assert isinstance(contact_message, ContactMessageDTO)


async def test_cannot_get_contact_message_invalid_id(
    contact_message_query_service: ContactMessageQueryService,
) -> None:
    with pytest.raises(InvalidContactMessageId):
        await contact_message_query_service.get_message(contact_message_id="test")


async def test_cannot_get_contact_message_not_found(
    contact_message_query_service: ContactMessageQueryService,
) -> None:
    with pytest.raises(ContactMessageNotFoundById):
        await contact_message_query_service.get_message(contact_message_id=str(uuid4()))
