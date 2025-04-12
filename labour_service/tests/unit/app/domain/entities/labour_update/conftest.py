from datetime import datetime
from uuid import UUID

import pytest

from app.labour.domain.labour_update.entity import LabourUpdate


@pytest.fixture
def sample_announcement() -> LabourUpdate:
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    sent_time: datetime = datetime(2020, 1, 1)
    return LabourUpdate.create(
        labour_id=labour_id,
        message="Test Message",
        sent_time=sent_time,
    )
