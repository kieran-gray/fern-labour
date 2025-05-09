import json

import pytest

from src.application.dtos import ContactMessageDTO
from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage
from src.domain.enums import ContactMessageCategory
from src.user.domain.value_objects.user_id import UserId


@pytest.fixture
def contact_message() -> ContactMessage:
    return ContactMessage(
        id_=ContactMessageId("test"),
        category=ContactMessageCategory.ERROR_REPORT,
        email="test@email.com",
        name="User Name",
        message="help me",
        data=None,
        user_id=UserId("abc123"),
    )


def test_can_convert_to_contact_message_dto(contact_message: ContactMessage) -> None:
    dto = ContactMessageDTO.from_domain(contact_message)
    assert dto.id == contact_message.id_.value
    assert dto.category == contact_message.category
    assert dto.email == contact_message.email
    assert dto.name == contact_message.name
    assert dto.message == contact_message.message
    assert dto.data == contact_message.data
    assert dto.user_id == contact_message.user_id.value


def test_can_convert_contact_message_dto_to_dict(contact_message: ContactMessage) -> None:
    dto = ContactMessageDTO.from_domain(contact_message)
    contact_message_dict = dto.to_dict()
    json.dumps(contact_message_dict)
