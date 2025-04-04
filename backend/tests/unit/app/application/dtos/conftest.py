from datetime import UTC, datetime

import pytest

from app.labour.domain.labour.entity import Labour
from app.user.domain.value_objects.user_id import UserId


@pytest.fixture
def sample_labour() -> Labour:
    return Labour.plan(
        birthing_person_id=UserId("test"), due_date=datetime.now(UTC), first_labour=True
    )
