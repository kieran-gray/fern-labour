from dataclasses import dataclass
from typing import Any, Self

from app.common.domain.event import DomainEvent


@dataclass
class NotificationRequested(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "notification.requested") -> Self:
        return super().create(event_type=event_type, data=data)
