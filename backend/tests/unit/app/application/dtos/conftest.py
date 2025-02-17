import pytest

from datetime import datetime, UTC
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour


@pytest.fixture
def sample_labour() -> Labour:
    return Labour.plan(
        birthing_person_id=BirthingPersonId("test"),
        due_date=datetime.now(UTC),
        first_labour=True
    )