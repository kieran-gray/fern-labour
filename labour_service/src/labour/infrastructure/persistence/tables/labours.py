import os

from sqlalchemy import Boolean, Column, DateTime, Enum, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.common.infrastructure.persistence.orm_registry import mapper_registry
from src.labour.domain.labour.enums import LabourPhase

labours_table = Table(
    "labours",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("birthing_person_id", String, nullable=False),
    Column("first_labour", Boolean, nullable=False),
    Column("due_date", DateTime(timezone=True), nullable=False),
    Column("labour_name", String, nullable=True),
    Column("payment_plan", String, nullable=True),
    Column("start_time", DateTime(timezone=True), nullable=True),
    Column("end_time", DateTime(timezone=True), nullable=True),
    Column("current_phase", Enum(LabourPhase, name="labour_phase"), nullable=False),
    Column(
        "notes",
        StringEncryptedType(
            type_in=String,
            key=os.getenv("DATABASE_ENCRYPTION_KEY"),  # TODO dependency injection
            engine=AesEngine,
            padding="pkcs5",
        ),
        nullable=True,
    ),
)
