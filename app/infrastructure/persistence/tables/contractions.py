from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.orm_registry import mapper_registry

contractions_table = Table(
    "contractions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labor_session_id", UUID(as_uuid=True), ForeignKey("labor_sessions.id"), nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime, nullable=False),
    Column("intensity", Integer, nullable=False),
    Column("notes", String, nullable=True),
    Column("created_at", DateTime, nullable=False, default=datetime.now()),
)
