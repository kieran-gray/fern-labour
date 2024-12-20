from uuid import UUID

import pytest
from datetime import datetime

from app.domain.labour.entity import Labour


@pytest.fixture
def sample_first_labor_session() -> Labour:
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    user_id: UUID = UUID("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()
    return Labour.begin(
        session_id=session_id,
        birthing_person_id=user_id,
        first_labor=True,
        start_time=start_time,
    )


@pytest.fixture
def sample_labor_session() -> Labour:
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    user_id: UUID = UUID("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()
    return Labour.begin(
        session_id=session_id,
        birthing_person_id=user_id,
        first_labor=False,
        start_time=start_time,
    )

