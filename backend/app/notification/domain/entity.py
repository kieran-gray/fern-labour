from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID, uuid4

from app.common.domain.aggregate_root import AggregateRoot
from app.notification.domain.enums import NotificationStatus, NotificationTemplate, NotificationType
from app.notification.domain.value_objects.notification_id import NotificationId


@dataclass(eq=False, kw_only=True)
class Notification(AggregateRoot[NotificationId]):
    status: NotificationStatus
    type: NotificationType
    destination: str
    template: str
    data: dict[str, Any]
    metadata: dict[str, Any] | None = None
    external_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        type: NotificationType,
        destination: str,
        template: NotificationTemplate,
        data: dict[str, Any],
        status: NotificationStatus | None = None,
        metadata: dict[str, Any] | None = None,
        external_id: str | None = None,
        notification_id: UUID | None = None,
    ) -> Self:
        notification_id = notification_id or uuid4()
        return cls(
            id_=NotificationId(notification_id),
            status=status or NotificationStatus.CREATED,
            type=type,
            destination=destination,
            template=template,
            data=data,
            metadata=metadata,
            external_id=external_id,
        )
