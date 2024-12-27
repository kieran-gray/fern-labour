from dataclasses import dataclass
from typing import Any, Self


@dataclass
class LabourPatternDTO:
    """Data Transfer Object for labor pattern analysis"""

    average_duration_minutes: float
    average_intensity: float
    average_interval_minutes: float
    phase: str

    @classmethod
    def from_domain(cls, pattern: dict[str, Any]) -> Self:
        """Create DTO from domain pattern dictionary"""
        return cls(
            average_duration_minutes=pattern["average_duration_minutes"],
            average_intensity=pattern["average_intensity"],
            average_interval_minutes=pattern["average_interval_minutes"],
            phase=pattern["phase"],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "average_duration_minutes": self.average_duration_minutes,
            "average_intensity": self.average_intensity,
            "average_interval_minutes": self.average_interval_minutes,
            "phase": self.phase,
        }
