from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID, uuid4

from fern_labour_core.aggregate_root import AggregateRoot

from src.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
)
from src.notification.domain.events import NotificationCreated, NotificationStatusUpdated
from src.notification.domain.value_objects.notification_id import NotificationId


@dataclass(eq=False, kw_only=True)
class Notification(AggregateRoot[NotificationId]):
    status: NotificationStatus
    channel: NotificationChannel
    destination: str
    template: str
    data: dict[str, Any]
    metadata: dict[str, Any] | None = None
    external_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        channel: NotificationChannel,
        destination: str,
        template: str,
        data: dict[str, Any],
        status: NotificationStatus | None = None,
        metadata: dict[str, Any] | None = None,
        external_id: str | None = None,
        notification_id: UUID | None = None,
    ) -> Self:
        notification_id = notification_id or uuid4()
        notification = cls(
            id_=NotificationId(notification_id),
            status=status or NotificationStatus.CREATED,
            channel=channel,
            destination=destination,
            template=template,
            data=data,
            metadata=metadata,
            external_id=external_id,
        )
        notification.add_domain_event(
            NotificationCreated.create(
                aggregate_id=str(notification_id),
                aggregate_type="notification",
                data={"notification_id": str(notification_id)},
            )
        )
        return notification

    def update_status(self, status: NotificationStatus) -> None:
        self.add_domain_event(
            NotificationStatusUpdated.create(
                aggregate_id=str(self.id_.value),
                aggregate_type="notification",
                data={
                    "notification_id": str(self.id_.value),
                    "channel": self.channel.value,
                    "external_id": self.external_id,
                    "from_status": self.status.value,
                    "to_status": status.value,
                },
            )
        )
        self.status = status
