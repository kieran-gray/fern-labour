from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.domain.labour_update.enums import LabourUpdateType
from app.infrastructure.persistence.orm_registry import mapper_registry

labour_updates_table = Table(
    "labour_updates",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labour_update_type", Enum(LabourUpdateType, name="labour_update_type"), nullable=False),
    Column("labour_id", UUID(as_uuid=True), ForeignKey("labours.id"), nullable=False),
    Column("message", String, nullable=False),
    Column("sent_time", DateTime(timezone=True), nullable=False),
)
