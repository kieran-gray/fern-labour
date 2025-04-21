from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite

from src.core.infrastructure.persistence.orm_registry import mapper_registry
from src.notification.domain.entity import Notification
from src.notification.domain.value_objects.notification_id import NotificationId
from src.notification.infrastructure.persistence.tables.notifications import notifications_table

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
        "metadata": notifications_table.c.metadata,
        "external_id": notifications_table.c.external_id,
    },
    column_prefix="_",
)


@event.listens_for(Notification, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
