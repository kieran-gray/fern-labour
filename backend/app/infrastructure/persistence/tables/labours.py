from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.domain.labour.enums import LabourPhase
from app.infrastructure.persistence.orm_registry import mapper_registry

labours_table = Table(
    "labours",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("birthing_person_id", String, ForeignKey("birthing_persons.id"), nullable=False),
    Column("first_labour", Boolean, nullable=False),
    Column("due_date", DateTime(timezone=True), nullable=False),
    Column("labour_name", String, nullable=True),
    Column("start_time", DateTime(timezone=True), nullable=True),
    Column("end_time", DateTime(timezone=True), nullable=True),
    Column("current_phase", Enum(LabourPhase, name="labour_phase"), nullable=False),
    Column("notes", String, nullable=True),
)
