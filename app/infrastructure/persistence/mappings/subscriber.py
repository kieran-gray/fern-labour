from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite

from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.subscribers import subscribers_table

mapper_registry.map_imperatively(
    Subscriber,
    subscribers_table,
    properties={
        "id_": composite(SubscriberId, subscribers_table.c.id),
        "first_name": subscribers_table.c.first_name,
        "last_name": subscribers_table.c.last_name,
        "phone_number": subscribers_table.c.phone_number,
        "email": subscribers_table.c.email,
        "contact_methods": subscribers_table.c.contact_methods,
        "subscribed_to": subscribers_table.c.subscribed_to,
    },
    column_prefix="_",
)


@event.listens_for(Subscriber, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
