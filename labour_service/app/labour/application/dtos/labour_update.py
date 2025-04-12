from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.labour.domain.labour_update.entity import LabourUpdate


@dataclass
class LabourUpdateDTO:
    """Data Transfer Object for Labour Update entity"""

    id: str
    labour_update_type: str
    labour_id: str
    message: str
    sent_time: datetime

    @classmethod
    def from_domain(cls, labour_update: LabourUpdate) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(labour_update.id_.value),
            labour_update_type=labour_update.labour_update_type.value,
            labour_id=str(labour_update.labour_id.value),
            message=labour_update.message,
            sent_time=labour_update.sent_time,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "labour_id": self.labour_id,
            "labour_update_type": self.labour_update_type,
            "message": self.message,
            "sent_time": self.sent_time.isoformat(),
        }
