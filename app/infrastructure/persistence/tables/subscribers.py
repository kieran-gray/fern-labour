from typing import Any

from sqlalchemy import ARRAY, Column, Enum, String, Table
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import String as type_String
from sqlalchemy.types import TypeDecorator

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.enums import ContactMethod
from app.infrastructure.persistence.orm_registry import mapper_registry


class BirthingPersonIdType(TypeDecorator[BirthingPersonId]):
    impl = type_String
    cache_ok = True

    def process_bind_param(self, birthing_person_id: BirthingPersonId | None, _: Any) -> str | None:
        return birthing_person_id.value if birthing_person_id else None

    def process_result_value(
        self, birthing_person_id: str | None, _: Any
    ) -> BirthingPersonId | None:
        return BirthingPersonId(birthing_person_id) if birthing_person_id else None


subscribers_table = Table(
    "subscribers",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("phone_number", String, nullable=True),
    Column("email", String, nullable=True),
    Column("contact_methods", ARRAY(Enum(ContactMethod)), default=[]),
    Column("subscribed_to", MutableList.as_mutable(ARRAY(BirthingPersonIdType)), default=[]),
)
