from sqlalchemy import ARRAY, Column, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.common.infrastructure.persistence.orm_registry import mapper_registry
from app.labour.domain.subscription.enums import ContactMethod, SubscriberRole, SubscriptionStatus

subscriptions_table = Table(
    "subscriptions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labour_id", UUID(as_uuid=True), ForeignKey("labours.id"), nullable=False),
    Column("birthing_person_id", String, nullable=False),
    Column("subscriber_id", String, nullable=False),
    Column("role", Enum(SubscriberRole, name="subscriber_role"), nullable=False),
    Column("status", Enum(SubscriptionStatus, name="subscription_status"), nullable=False),
    Column("contact_methods", ARRAY(Enum(ContactMethod)), default=[]),
)
