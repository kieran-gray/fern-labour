import os

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.core.infrastructure.persistence.orm_registry import mapper_registry
from src.labour.domain.labour_update.enums import LabourUpdateType

labour_updates_table = Table(
    "labour_updates",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("labour_update_type", Enum(LabourUpdateType, name="labour_update_type"), nullable=False),
    Column("labour_id", UUID(as_uuid=True), ForeignKey("labours.id"), nullable=False),
    Column(
        "message",
        StringEncryptedType(
            type_in=String,
            key=os.getenv("DATABASE_ENCRYPTION_KEY"),  # TODO dependency injection
            engine=AesEngine,
            padding="pkcs5",
        ),
        nullable=False,
    ),
    Column("sent_time", DateTime(timezone=True), nullable=False),
)
