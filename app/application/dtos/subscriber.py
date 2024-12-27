from dataclasses import dataclass
from typing import Any, Self

from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.enums import ContactMethod


@dataclass
class SubscriberDTO:
    id: str
    first_name: str
    last_name: str
    phone_number: str | None
    email: str | None
    contact_methods: list[str]
    subscribed_to: list[str]

    @classmethod
    def from_domain(cls, subscriber: Subscriber) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(subscriber.id_.value),
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
            phone_number=subscriber.phone_number,
            email=subscriber.email,
            contact_methods=[method.value for method in subscriber.contact_methods],
            subscribed_to=[
                birthing_person_id.value for birthing_person_id in subscriber.subscribed_to
            ],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "contact_methods": self.contact_methods,
            "subscribed_to": self.subscribed_to,
        }

    def destination(self, contact_method: str) -> str | None:
        contact_method_enum = ContactMethod(contact_method)
        if contact_method_enum is ContactMethod.SMS:
            return self.phone_number
        if contact_method_enum is ContactMethod.EMAIL:
            return self.email
        return None
