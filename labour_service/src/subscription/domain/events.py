from dataclasses import dataclass
from typing import Any, Self

from src.core.domain.event import DomainEvent


@dataclass
class SubscriberRequested(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "subscriber.requested") -> Self:
        return super().create(event_type=event_type, data=data)


@dataclass
class SubscriberApproved(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "subscriber.approved") -> Self:
        return super().create(event_type=event_type, data=data)
