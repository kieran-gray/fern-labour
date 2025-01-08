import json
from uuid import UUID, uuid4

import pytest

from app.application.dtos.announcement import AnnouncementDTO
from app.domain.announcement.entity import Announcement
from app.domain.labour.vo_labour_id import LabourId


@pytest.fixture
def announcement() -> Announcement:
    return Announcement.create(labour_id=LabourId(uuid4()), message="Test Message")


def test_can_convert_to_announcement_dto(announcement: Announcement) -> None:
    dto = AnnouncementDTO.from_domain(announcement)
    assert UUID(dto.labour_id) == announcement.labour_id.value
    assert dto.sent_time == announcement.sent_time
    assert dto.message == announcement.message
    assert UUID(dto.id) == announcement.id_.value


def test_can_convert_announcement_dto_to_dict(announcement: Announcement) -> None:
    dto = AnnouncementDTO.from_domain(announcement)
    announcement_dict = dto.to_dict()
    json.dumps(announcement_dict)  # Check dict is json serializable
