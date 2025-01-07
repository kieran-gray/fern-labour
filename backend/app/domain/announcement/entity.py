from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.announcement.vo_announcement_id import AnnouncementId
from app.domain.base.entity import Entity
from app.domain.labour.vo_labour_id import LabourId


@dataclass(eq=False, kw_only=True)
class Announcement(Entity[AnnouncementId]):
    labour_id: LabourId
    message: str
    sent_time: datetime

    @classmethod
    def create(
        cls,
        *,
        labour_id: LabourId,
        message: str,
        sent_time: datetime | None = None,
        announcement_id: UUID | None = None,
    ) -> Self:
        sent_time = sent_time or datetime.now(UTC)
        announcement_id = announcement_id or uuid4()
        return cls(
            id_=AnnouncementId(announcement_id),
            labour_id=labour_id,
            message=message,
            sent_time=sent_time,
        )
