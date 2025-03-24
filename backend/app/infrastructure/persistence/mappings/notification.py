from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite

from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.vo_labour_update_id import LabourUpdateId
from app.domain.notification.entity import Notification
from app.domain.notification.vo_notification_id import NotificationId
from app.domain.user.vo_user_id import UserId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.notifications import notifications_table

mapper_registry.map_imperatively(
    Notification,
    notifications_table,
    properties={
        "id_": composite(NotificationId, notifications_table.c.id),
        "status": notifications_table.c.status,
        "type": notifications_table.c.type,
        "destination": notifications_table.c.destination,
        "template": notifications_table.c.template,
        "data": notifications_table.c.data,
        "labour_id": composite(LabourId, notifications_table.c.labour_id),
        "birthing_person_id": composite(UserId, notifications_table.c.birthing_person_id),
        "subscriber_id": composite(UserId, notifications_table.c.subscriber_id),
        "labour_update_id": composite(LabourUpdateId, notifications_table.c.labour_update_id),
    },
    column_prefix="_",
)


@event.listens_for(Notification, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
