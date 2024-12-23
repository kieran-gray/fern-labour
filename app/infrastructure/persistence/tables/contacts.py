from sqlalchemy import ARRAY, UUID, Column, Enum, ForeignKey, String, Table

from app.domain.contact.enums import ContactMethod
from app.infrastructure.persistence.orm_registry import mapper_registry

contacts_table = Table(
    "contacts",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("birthing_person_id", String, ForeignKey("birthing_persons.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("phone_number", String, nullable=True),
    Column("email", String, nullable=True),
    Column("contact_methods", ARRAY(Enum(ContactMethod)), default=[]),
)
