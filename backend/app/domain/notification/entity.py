from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID, uuid4

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.vo_labour_update_id import LabourUpdateId
from app.domain.notification.enums import NotificationStatus
from app.domain.notification.vo_notification_id import NotificationId
from app.domain.subscription.enums import ContactMethod
from app.domain.user.vo_user_id import UserId


@dataclass(eq=False, kw_only=True)
class Notification(AggregateRoot[NotificationId]):
    status: NotificationStatus
    type: ContactMethod
    destination: str
    template: str
    data: dict[str, Any]
    labour_id: LabourId | None = None
    birthing_person_id: UserId | None = None
    subscriber_id: UserId | None = None
    labour_update_id: LabourUpdateId | None = None

    @classmethod
    def create(
        cls,
        *,
        type: ContactMethod,
        destination: str,
        template: str,
        data: dict[str, Any],
        status: NotificationStatus | None = None,
        labour_id: LabourId | None = None,
        birthing_person_id: UserId | None = None,
        subscriber_id: UserId | None = None,
        labour_update_id: LabourUpdateId | None = None,
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
            birthing_person_id=birthing_person_id,
            subscriber_id=subscriber_id,
            labour_update_id=labour_update_id,
        )

    def update_status(self, status: NotificationStatus) -> None:
        self.status = status
