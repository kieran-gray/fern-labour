from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.orm_registry import mapper_registry

announcements_table = Table(
    "announcements",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labour_id", UUID(as_uuid=True), ForeignKey("labours.id"), nullable=False),
    Column("message", String, nullable=False),
    Column("sent_time", DateTime(timezone=True), nullable=False),
)
