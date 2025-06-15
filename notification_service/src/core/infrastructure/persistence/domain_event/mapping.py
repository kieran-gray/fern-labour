from fern_labour_core.events.event import DomainEvent
from fern_labour_notifications_shared.events import NotificationRequested

from src.core.infrastructure.persistence.domain_event.table import domain_events_table
from src.core.infrastructure.persistence.orm_registry import mapper_registry
from src.notification.domain.events import NotificationStatusUpdated


def map_domain_events_table() -> None:
    domain_event_mapper = mapper_registry.map_imperatively(
        DomainEvent,
        domain_events_table,
        properties={
            "id": domain_events_table.c.event_id,
            "aggregate_id": domain_events_table.c.aggregate_id,
            "aggregate_type": domain_events_table.c.aggregate_type,
            "type": domain_events_table.c.type,
            "data": domain_events_table.c.data,
            "time": domain_events_table.c.created_at,
        },
        column_prefix="_",
        polymorphic_on=domain_events_table.c.type,
    )
    mapper_registry.map_imperatively(
        NotificationRequested,
        inherits=domain_event_mapper,
        polymorphic_identity="notification.requested",
    )
    mapper_registry.map_imperatively(
        NotificationStatusUpdated,
        inherits=domain_event_mapper,
        polymorphic_identity="notification.status-updated",
    )
