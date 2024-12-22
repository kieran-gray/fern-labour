from dataclasses import dataclass
from typing import Any, Self

from app.domain.contact.entity import Contact


@dataclass
class ContactDTO:
    id: str
    name: str
    phone_number: str | None
    email: str | None
    contact_methods: list[str]

    @classmethod
    def from_domain(cls, contact: Contact) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(contact.id_.value),
            name=contact.name,
            phone_number=contact.phone_number,
            email=contact.email,
            contact_methods=[method.value for method in contact.contact_methods],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "contact_methods": self.contact_methods,
        }
