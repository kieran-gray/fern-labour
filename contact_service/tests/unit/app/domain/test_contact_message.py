from uuid import UUID

from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage
from src.domain.enums import ContactMessageCategory
from src.user.domain.value_objects.user_id import UserId


def test_contact_message_init():
    contact_message_id = UUID("12345678-1234-5678-1234-567812345678")
    user_id = UserId("87654321-4321-1234-8765-567812345678")
    email = "test@email.com"
    name = "User Name"
    message = "help me"
    data = {"test": "data"}

    vo_contact_message_id = ContactMessageId(contact_message_id)

    direct_contact_message = ContactMessage(
        id_=vo_contact_message_id,
        category=ContactMessageCategory.ERROR_REPORT,
        email=email,
        name=name,
        message=message,
        data=data,
        user_id=user_id,
    )

    indirect_contact_message = ContactMessage.create(
        contact_message_id=contact_message_id,
        category=ContactMessageCategory.ERROR_REPORT,
        email=email,
        name=name,
        message=message,
        data=data,
        user_id=user_id,
    )

    assert isinstance(indirect_contact_message, ContactMessage)
    assert direct_contact_message.id_ == vo_contact_message_id == indirect_contact_message.id_
    assert direct_contact_message == indirect_contact_message
