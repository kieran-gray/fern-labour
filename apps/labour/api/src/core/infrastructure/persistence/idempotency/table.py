from enum import StrEnum

from sqlalchemy import Column, DateTime, Enum, String, Table, func

from src.core.infrastructure.persistence.orm_registry import mapper_registry


class ProcessingStatus(StrEnum):
    """Defines the processing status of an event."""

    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


consumer_processed_events_table = Table(
    "consumer_processed_events",
    mapper_registry.metadata,
    Column("event_id", String, primary_key=True, nullable=False),
    Column(
        "status",
        Enum(ProcessingStatus, name="processing_status_enum"),
        nullable=False,
        default=ProcessingStatus.PROCESSING,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
)
