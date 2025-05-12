from dataclasses import dataclass
from typing import Any, Self

from src.domain.entity import ContactMessage


@dataclass
class ContactMessageDTO:
    id: str
    category: str
    email: str
    name: str
    message: str
    data: dict[str, Any] | None = None
    user_id: str | None = None

    @classmethod
    def from_domain(cls, contact_message: ContactMessage) -> Self:
        return cls(
            id=str(contact_message.id_.value),
            category=contact_message.category.value,
            email=contact_message.email,
            name=contact_message.name,
            message=contact_message.message,
            data=contact_message.data,
            user_id=contact_message.user_id.value if contact_message.user_id else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "email": self.email,
            "name": self.name,
            "message": self.message,
            "data": self.data,
            "user_id": self.user_id,
        }
