from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite

from app.common.infrastructure.persistence.orm_registry import mapper_registry
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId
from app.notification.domain.entity import Notification
from app.notification.domain.value_objects.notification_id import NotificationId
from app.notification.infrastructure.persistence.tables.notifications import notifications_table
from app.user.domain.value_objects.user_id import UserId

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
        "from_user_id": composite(UserId, notifications_table.c.from_user_id),
        "to_user_id": composite(UserId, notifications_table.c.to_user_id),
        "labour_update_id": composite(LabourUpdateId, notifications_table.c.labour_update_id),
        "external_id": notifications_table.c.external_id,
    },
    column_prefix="_",
)


@event.listens_for(Notification, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
