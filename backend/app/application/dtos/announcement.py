from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.domain.announcement.entity import Announcement


@dataclass
class AnnouncementDTO:
    """Data Transfer Object for Announcement entity"""

    id: str
    labour_id: str
    message: str
    sent_time: datetime

    @classmethod
    def from_domain(cls, announcement: Announcement) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(announcement.id_.value),
            labour_id=str(announcement.labour_id.value),
            message=announcement.message,
            sent_time=announcement.sent_time,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "labour_id": self.labour_id,
            "message": self.message,
            "sent_time": self.sent_time.isoformat(),
        }
