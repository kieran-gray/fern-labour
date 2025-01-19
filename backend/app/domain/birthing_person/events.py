from dataclasses import dataclass
from typing import Any, Self

from app.domain.base.event import DomainEvent


@dataclass
class RemovedSubscriber(DomainEvent):
    @classmethod
    def create(
        cls, data: dict[str, Any], event_type: str = "birthing-person.removed-subscriber"
    ) -> Self:
        return super().create(event_type=event_type, data=data)
