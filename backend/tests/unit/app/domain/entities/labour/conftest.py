from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.domain.labour.entity import Labour


@pytest.fixture
def sample_first_labour() -> Labour:
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    birthing_person_id = "87654321-4321-1234-8765-567812345678"
    start_time: datetime = datetime.now(UTC)
    return Labour.begin(
        labour_id=labour_id,
        birthing_person_id=birthing_person_id,
        first_labour=True,
        start_time=start_time,
    )


@pytest.fixture
def sample_labour() -> Labour:
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    birthing_person_id = "87654321-4321-1234-8765-567812345678"
    start_time: datetime = datetime.now(UTC)
    return Labour.begin(
        labour_id=labour_id,
        birthing_person_id=birthing_person_id,
        first_labour=False,
        start_time=start_time,
    )
