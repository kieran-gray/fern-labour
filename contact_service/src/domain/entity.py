from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID, uuid4

from fern_labour_core.aggregate_root import AggregateRoot

from src.domain.contact_message_id import ContactMessageId
from src.domain.enums import ContactMessageCategory
from src.domain.events import ContactMessageCreated
from src.user.domain.value_objects.user_id import UserId


@dataclass(eq=False, kw_only=True)
class ContactMessage(AggregateRoot[ContactMessageId]):
    category: ContactMessageCategory
    email: str
    name: str
    message: str
    data: dict[str, Any] | None = None
    user_id: UserId | None = None

    @classmethod
    def create(
        cls,
        *,
        category: ContactMessageCategory,
        email: str,
        name: str,
        message: str,
        data: dict[str, Any] | None = None,
        user_id: UserId | None = None,
        contact_message_id: UUID | None = None,
    ) -> Self:
        contact_message_id = contact_message_id or uuid4()
        contact_message = cls(
            id_=ContactMessageId(contact_message_id),
            category=category,
            email=email,
            name=name,
            message=message,
            data=data,
            user_id=user_id,
        )
        contact_message.add_domain_event(
            ContactMessageCreated.create(data={"contact_message_id": str(contact_message_id)})
        )
        return contact_message
