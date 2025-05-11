from dataclasses import dataclass
from typing import Any, Self

from fern_labour_core.events.event import DomainEvent


@dataclass
class ContactMessageSubmitted(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "contact-message.submitted") -> Self:
        return super().create(event_type=event_type, data=data)
