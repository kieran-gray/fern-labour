from dataclasses import dataclass
from typing import Any, Self

from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationStatus


@dataclass
class NotificationSendResult:
    success: bool
    status: NotificationStatus
    external_id: str | None = None


@dataclass
class NotificationContent:
    message: str
    subject: str | None = None


@dataclass
class NotificationDTO:
    """Data Transfer Object for Notification aggregate"""

    id: str
    status: str
    type: str
    destination: str
    template: str
    data: dict[str, Any]
    metadata: dict[str, Any] | None = None
    external_id: str | None = None
    message: str | None = None
    subject: str | None = None

    def add_notification_content(self, content: NotificationContent) -> None:
        self.message = content.message
        self.subject = content.subject

    @classmethod
    def from_domain(cls, notification: Notification) -> Self:
        """Create DTO from domain aggregate"""

        return cls(
            id=str(notification.id_.value),
            status=notification.status,
            type=notification.type,
            destination=notification.destination,
            template=notification.template,
            data=notification.data,
            metadata=notification.metadata,
            external_id=notification.external_id,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "status": self.status,
            "type": self.type,
            "destination": self.destination,
            "template": self.template,
            "data": self.data,
            "metadata": self.metadata,
            "external_id": self.external_id,
        }
