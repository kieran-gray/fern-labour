from datetime import datetime
from uuid import UUID

import pytest

from app.domain.announcement.entity import Announcement


@pytest.fixture
def sample_announcement() -> Announcement:
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    sent_time: datetime = datetime(2020, 1, 1)
    return Announcement.create(
        labour_id=labour_id,
        message="Test Message",
        sent_time=sent_time,
    )
