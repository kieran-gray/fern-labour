from dataclasses import dataclass
from typing import Any, Self

from src.core.domain.event import DomainEvent


@dataclass
class NotificationRequestedData:
    type: str
    destination: str
    template: str
    data: dict[str, Any]
    metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, event_data: dict[str, Any]) -> Self:
        return cls(
            type=event_data["type"],
            destination=event_data["destination"],
            template=event_data["template"],
            data=event_data["data"],
            metadata=event_data["metadata"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
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


@dataclass
class NotificationStatusUpdatedData:
    notification_id: str
    from_status: str
    to_status: str
    external_id: str | None = None

    @classmethod
    def from_dict(cls, event_data: dict[str, Any]) -> Self:
        return cls(
            notification_id=event_data["notification_id"],
            from_status=event_data["from_status"],
            to_status=event_data["to_status"],
            external_id=event_data["external_id"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "external_id": self.external_id,
        }


@dataclass
class NotificationStatusUpdated(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "notification.status-updated") -> Self:
        return super().create(event_type=event_type, data=data)
