from dataclasses import dataclass
from typing import Any, Self


@dataclass
class LabourPatternDTO:
    """Data Transfer Object for labor pattern analysis"""

    average_duration: float
    average_intensity: float
    average_interval: float
    phase: str

    @classmethod
    def from_domain(cls, pattern: dict[str, Any]) -> Self:
        """Create DTO from domain pattern dictionary"""
        return cls(
            average_duration=pattern["average_duration"],
            average_intensity=pattern["average_intensity"],
            average_interval=pattern["average_interval"],
            phase=pattern["phase"],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "average_duration": self.average_duration,
            "average_intensity": self.average_intensity,
            "average_interval": self.average_interval,
            "phase": self.phase,
        }
