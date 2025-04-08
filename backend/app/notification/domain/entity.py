from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID, uuid4

from app.common.domain.aggregate_root import AggregateRoot
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId
from app.notification.domain.enums import NotificationStatus, NotificationTemplate
from app.notification.domain.value_objects.notification_id import NotificationId
from app.subscription.domain.enums import ContactMethod
from app.user.domain.value_objects.user_id import UserId


@dataclass(eq=False, kw_only=True)
class Notification(AggregateRoot[NotificationId]):
    status: NotificationStatus
    type: ContactMethod
    destination: str
    template: str
    data: dict[str, Any]
    labour_id: LabourId | None = None
    from_user_id: UserId | None = None
    to_user_id: UserId | None = None
    labour_update_id: LabourUpdateId | None = None
    external_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        type: ContactMethod,
        destination: str,
        template: NotificationTemplate,
        data: dict[str, Any],
        status: NotificationStatus | None = None,
        labour_id: LabourId | None = None,
        from_user_id: UserId | None = None,
        to_user_id: UserId | None = None,
        labour_update_id: LabourUpdateId | None = None,
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
            labour_id=labour_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            labour_update_id=labour_update_id,
            external_id=external_id,
        )
