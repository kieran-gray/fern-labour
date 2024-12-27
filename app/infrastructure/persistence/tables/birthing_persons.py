from typing import Any

from sqlalchemy import ARRAY, Boolean, Column, DateTime, String, Table, text
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import String as type_String
from sqlalchemy.types import TypeDecorator

from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.infrastructure.persistence.orm_registry import mapper_registry


class SubscriberIdType(TypeDecorator[SubscriberId]):
    impl = type_String
    cache_ok = True

    def process_bind_param(self, subscriber_id: SubscriberId | None, _: Any) -> str | None:
        return subscriber_id.value if subscriber_id else None

    def process_result_value(self, subscriber_id: str | None, _: Any) -> SubscriberId | None:
        return SubscriberId(subscriber_id) if subscriber_id else None


birthing_persons_table = Table(
    "birthing_persons",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("first_labour", Boolean, nullable=True),
    Column("subscribers", MutableList.as_mutable(ARRAY(SubscriberIdType)), default=[]),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
)
