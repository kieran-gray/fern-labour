from datetime import UTC, datetime

import pytest

from app.domain.user.vo_user_id import UserId
from app.labour.domain.labour.entity import Labour


@pytest.fixture
def sample_labour() -> Labour:
    return Labour.plan(
        birthing_person_id=UserId("test"), due_date=datetime.now(UTC), first_labour=True
    )
