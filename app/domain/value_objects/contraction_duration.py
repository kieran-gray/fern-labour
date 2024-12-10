from dataclasses import dataclass
from datetime import datetime

from app.domain.base.value_object import ValueObject
from app.domain.constants.contraction import CONTRACTION_MAX_TIME, CONTRACTION_MIN_TIME
from app.domain.exceptions.contraction import (
    ContractionDurationExceedsMaxDuration,
    ContractionDurationLessThanMinDuration,
    ContractionStartTimeAfterEndTime,
)


@dataclass(frozen=True)
class Duration(ValueObject):
    """
    Value object representing the duration of a contraction.
    Includes start and end time to calculate duration and validate time spans.
    """

    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        """Validate the duration upon initialization"""
        super().__post_init__()

        if self.start_time == self.end_time:
            # Temp duration
            return

        if self.start_time > self.end_time:
            raise ContractionStartTimeAfterEndTime()

        duration = self.end_time - self.start_time

        if duration > CONTRACTION_MAX_TIME:
            raise ContractionDurationExceedsMaxDuration()

        if duration < CONTRACTION_MIN_TIME:
            raise ContractionDurationLessThanMinDuration()

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
