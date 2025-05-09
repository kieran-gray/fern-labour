from sqlalchemy import Column, Enum, String, Table
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.sql import func

from src.domain.enums import ContactMessageCategory
from src.infrastructure.persistence.orm_registry import mapper_registry

contact_messages_table = Table(
    "contact_messages",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "category", Enum(ContactMessageCategory, name="contact_message_category"), nullable=False
    ),
    Column("email", String, nullable=False),
    Column("name", String, nullable=False),
    Column("message", String, nullable=False),
    Column("data", JSONB, nullable=True),
    Column("user_id", String, nullable=True),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
)
