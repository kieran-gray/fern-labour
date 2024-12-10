from uuid import UUID

import pytest
from datetime import datetime

from app.domain.entities.labor_session import LaborSession


@pytest.fixture
def sample_first_labor_session() -> LaborSession:
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    user_id: UUID = UUID("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()
    return LaborSession.start(
        session_id=session_id,
        user_id=user_id,
        first_labor=True,
        start_time=start_time,
    )


@pytest.fixture
def sample_labor_session() -> LaborSession:
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    user_id: UUID = UUID("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()
    return LaborSession.start(
        session_id=session_id,
        user_id=user_id,
        first_labor=False,
        start_time=start_time,
    )

