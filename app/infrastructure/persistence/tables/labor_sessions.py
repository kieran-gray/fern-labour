from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.domain.entities.labor_session import LaborPhase
from app.infrastructure.persistence.orm_registry import mapper_registry

labor_sessions_table = Table(
    "labor_sessions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime, nullable=True),
    Column("current_phase", Enum(LaborPhase, name="labor_phase"), nullable=False),
    Column("notes", String, nullable=True),
    Column("created_at", DateTime, nullable=False, default=datetime.now()),
)
