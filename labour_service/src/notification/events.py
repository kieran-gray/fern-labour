from dataclasses import dataclass
from typing import Any, Self

from src.core.domain.event import DomainEvent


@dataclass
class NotificationRequestedData:
    channel: str
    destination: str
    template: str
    data: dict[str, Any]
    metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, event_data: dict[str, Any]) -> Self:
        return cls(
            channel=event_data["channel"],
            destination=event_data["destination"],
            template=event_data["template"],
            data=event_data["data"],
            metadata=event_data["metadata"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel": self.channel,
            "destination": self.destination,
            "template": self.template,
            "data": self.data,
            "metadata": self.metadata,
        }


@dataclass
class NotificationRequested(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "notification.requested") -> Self:
        return super().create(event_type=event_type, data=data)
