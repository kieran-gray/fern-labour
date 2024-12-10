from dataclasses import dataclass


@dataclass
class LaborPatternDTO:
    """Data Transfer Object for labor pattern analysis"""

    average_duration_minutes: float
    average_intensity: float
    average_interval_minutes: float
    phase: str
    hospital_recommended: bool

    @classmethod
    def from_domain(cls, pattern: dict) -> "LaborPatternDTO":
        """Create DTO from domain pattern dictionary"""
        return cls(
            average_duration_minutes=pattern["average_duration_minutes"],
            average_intensity=pattern["average_intensity"],
            average_interval_minutes=pattern["average_interval_minutes"],
            phase=pattern["phase"],
            hospital_recommended=pattern["hospital_recommended"],
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "average_duration_minutes": self.average_duration_minutes,
            "average_intensity": self.average_intensity,
            "average_interval_minutes": self.average_interval_minutes,
            "phase": self.phase,
            "hospital_recommended": self.hospital_recommended,
        }
