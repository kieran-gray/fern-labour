from dataclasses import dataclass
from typing import Any, Self

from app.domain.base.event import DomainEvent


@dataclass
class SubscriberSubscribedTo(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "subscriber.subscribed-to") -> Self:
        return super().create(event_type=event_type, data=data)


@dataclass
class SubscriberUnsubscribedFrom(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "subscriber.unsubscribed-from") -> Self:
        return super().create(event_type=event_type, data=data)
