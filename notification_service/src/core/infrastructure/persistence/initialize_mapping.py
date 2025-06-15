from src.core.infrastructure.persistence.domain_event.mapping import map_domain_events_table
from src.notification.infrastructure.persistence.mapping import (
    map_notifications_table,
)


def map_all() -> None:
    map_notifications_table()
    map_domain_events_table()
