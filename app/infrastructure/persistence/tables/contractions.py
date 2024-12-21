from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.orm_registry import mapper_registry

contractions_table = Table(
    "contractions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labour_id", UUID(as_uuid=True), ForeignKey("labours.id"), nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime, nullable=False),
    Column("intensity", Integer, nullable=True),
    Column("notes", String, nullable=True),
)
