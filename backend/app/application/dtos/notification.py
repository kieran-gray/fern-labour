from dataclasses import dataclass
from typing import Any, Self

from app.domain.notification.entity import Notification
from app.domain.notification.enums import NotificationStatus


@dataclass
class NotificationSendResult:
    success: bool
    status: NotificationStatus


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
    labour_id: str | None = None
    birthing_person_id: str | None = None
    subscriber_id: str | None = None
    labour_update_id: str | None = None
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
            labour_id=str(notification.labour_id.value) if notification.labour_id else None,
            birthing_person_id=notification.birthing_person_id.value
            if notification.birthing_person_id
            else None,
            subscriber_id=notification.subscriber_id.value if notification.subscriber_id else None,
            labour_update_id=str(notification.labour_update_id)
            if notification.labour_update_id
            else None,
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
            "labour_id": self.labour_id,
            "birthing_person_id": self.birthing_person_id,
            "subscriber_id": self.subscriber_id,
            "labour_update_id": self.labour_update_id,
        }
