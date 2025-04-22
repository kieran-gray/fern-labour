from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from src.core.domain.value_object import ValueObject
from src.labour.domain.contraction.exceptions import ContractionStartTimeAfterEndTime


@dataclass(frozen=True)
class Duration(ValueObject):
    """
    Value object representing the duration of a contraction.
    Includes start and end time to calculate duration and validate time spans.
    """

    start_time: datetime
    end_time: datetime

    @classmethod
    def create(cls, *, start_time: datetime, end_time: datetime) -> Self:
        def ensure_timezone_aware(dt: datetime) -> datetime:
            """Ensures a datetime is timezone-aware by adding UTC if necessary."""
            if dt.tzinfo is None:
                return dt.replace(tzinfo=UTC)
            return dt

        return cls(
            start_time=ensure_timezone_aware(start_time),
            end_time=ensure_timezone_aware(end_time),
        )

    def __post_init__(self) -> None:
        """Validate the duration upon initialization"""
        super().__post_init__()

        if self.start_time == self.end_time:
            # Temp duration
            return

        if self.start_time > self.end_time:
            raise ContractionStartTimeAfterEndTime()

    @property
    def duration_seconds(self) -> float:
        """Get the duration in seconds"""
        return (self.end_time - self.start_time).total_seconds()

    @property
    def duration_minutes(self) -> float:
        """Get the duration in minutes"""
        return self.duration_seconds / 60

    def __str__(self) -> str:
        """String representation showing duration in minutes and seconds"""
        total_seconds = int(self.duration_seconds)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
