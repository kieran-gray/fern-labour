from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite

from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.vo_subscription_id import SubscriptionId
from app.domain.user.vo_user_id import UserId
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.subscriptions import subscriptions_table

mapper_registry.map_imperatively(
    Subscription,
    subscriptions_table,
    properties={
        "id_": composite(SubscriptionId, subscriptions_table.c.id),
        "labour_id": composite(LabourId, subscriptions_table.c.labour_id),
        "birthing_person_id": composite(UserId, subscriptions_table.c.birthing_person_id),
        "subscriber_id": composite(UserId, subscriptions_table.c.subscriber_id),
        "role": subscriptions_table.c.role,
        "status": subscriptions_table.c.status,
        "contact_methods": subscriptions_table.c.contact_methods,
    },
    column_prefix="_",
)


@event.listens_for(Subscription, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
