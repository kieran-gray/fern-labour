from dataclasses import dataclass
from typing import Any, Self

from app.labour.domain.subscription.entity import Subscription


@dataclass
class SubscriptionDTO:
    id: str
    labour_id: str
    birthing_person_id: str
    subscriber_id: str
    role: str
    status: str
    contact_methods: list[str]

    @classmethod
    def from_domain(cls, subscription: Subscription) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(subscription.id_.value),
            labour_id=str(subscription.labour_id.value),
            birthing_person_id=subscription.birthing_person_id.value,
            subscriber_id=subscription.subscriber_id.value,
            role=subscription.role.value,
            status=subscription.status.value,
            contact_methods=[method.value for method in subscription.contact_methods],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "labour_id": self.labour_id,
            "birthing_person_id": self.birthing_person_id,
            "subscriber_id": self.subscriber_id,
            "role": self.role,
            "status": self.status,
            "contact_methods": self.contact_methods,
        }
