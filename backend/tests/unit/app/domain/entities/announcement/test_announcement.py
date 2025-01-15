from datetime import UTC, datetime
from uuid import UUID

from app.domain.announcement.entity import Announcement
from app.domain.announcement.vo_announcement_id import AnnouncementId
from app.domain.labour.vo_labour_id import LabourId


def test_announcement_init():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    announcement_id: UUID = UUID("87654321-1234-5678-1234-567812345678")
    sent_time: datetime = datetime.now(UTC)
    message: str = "Test Message"

    vo_announcement_id = AnnouncementId(announcement_id)

    direct_announcement = Announcement(
        id_=vo_announcement_id, labour_id=labour_id, message=message, sent_time=sent_time
    )

    indirect_announcement = Announcement.create(
        announcement_id=announcement_id, labour_id=labour_id, message=message, sent_time=sent_time
    )

    assert isinstance(indirect_announcement, Announcement)
    assert direct_announcement.id_ == vo_announcement_id == indirect_announcement.id_
    assert direct_announcement == indirect_announcement


def test_announcement_init_default_values():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    message: str = "Test user"

    announcement = Announcement.create(labour_id=labour_id, message=message)
    assert isinstance(announcement, Announcement)
    assert announcement.sent_time is not None
    assert announcement.id_ is not None
