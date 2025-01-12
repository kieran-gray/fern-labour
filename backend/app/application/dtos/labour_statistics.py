from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Self

from app.domain.contraction.entity import Contraction


@dataclass
class LabourStatisticsDTO:
    """Data Transfer Object for labour statistics"""

    last_30_mins: LabourStatisticsDataDTO | None = None
    last_60_mins: LabourStatisticsDataDTO | None = None
    total: LabourStatisticsDataDTO | None = None

    @classmethod
    def from_contractions(cls, contractions: list[Contraction]) -> Self:
        """Create DTO from list of contractions"""

        def filter_contractions(
            contractions: list[Contraction], delta: timedelta
        ) -> list[Contraction]:
            return [c for c in contractions if c.start_time >= datetime.now(UTC) - delta]

        statistics = cls()
        if len(contractions) < 3:
            return statistics

        if contractions_30_min := filter_contractions(contractions, timedelta(minutes=30)):
            statistics.last_30_mins = LabourStatisticsDataDTO.from_contractions(contractions_30_min)

        if contractions_60_min := filter_contractions(contractions, timedelta(minutes=60)):
            statistics.last_60_mins = LabourStatisticsDataDTO.from_contractions(contractions_60_min)

        statistics.total = LabourStatisticsDataDTO.from_contractions(contractions)

        return statistics

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "last_30_mins": self.last_30_mins.to_dict() if self.last_30_mins else None,
            "last_60_mins": self.last_60_mins.to_dict() if self.last_60_mins else None,
            "total": self.total.to_dict() if self.total else None,
        }


@dataclass
class LabourStatisticsDataDTO:
    """Data Transfer Object for labour statistics data analysis"""

    contraction_count: int
    average_duration: float
    average_intensity: float
    average_frequency: float

    @classmethod
    def from_contractions(cls, contractions: list[Contraction]) -> Self:
        """Create DTO from contractions pattern dictionary"""
        contraction_intensities = []
        contraction_durations = []

        for contraction in contractions:
            if duration := contraction.duration.duration_seconds:
                contraction_durations.append(duration)
            if intensity := contraction.intensity:
                contraction_intensities.append(intensity)

        avg_duration = 0.0
        if contraction_durations:
            avg_duration = sum(contraction_durations) / len(contraction_durations)

        avg_intensity = 0.0
        if contraction_intensities:
            avg_intensity = sum(contraction_intensities) / len(contraction_intensities)

        # Calculate frequency of contractions
        # The frequency of a contraction is the gap between the start of 2 contractions
        frequencies = []
        for prev, curr in zip(contractions, contractions[1:], strict=False):
            frequency = (curr.start_time - prev.start_time).total_seconds()
            frequencies.append(frequency)

        avg_frequency = 0.0
        if frequencies:
            avg_frequency = sum(frequencies) / len(frequencies)

        return cls(
            average_duration=avg_duration,
            average_intensity=avg_intensity,
            average_frequency=avg_frequency,
            contraction_count=len(contractions),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "average_duration": self.average_duration,
            "average_intensity": self.average_intensity,
            "average_frequency": self.average_frequency,
            "contraction_count": self.contraction_count,
        }
