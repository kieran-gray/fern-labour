from datetime import UTC, datetime

import pytest

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.labour.entity import Labour


@pytest.fixture
def sample_birthing_person() -> BirthingPerson:
    birthing_person_id = "12345678-1234-5678-1234-567812345678"
    return BirthingPerson.create(
        birthing_person_id=birthing_person_id,
        first_name="User",
        last_name="Name",
    )


@pytest.fixture
def sample_labour(sample_birthing_person: BirthingPerson) -> Labour:
    labour_id = "12345678-abcd-efgh-ijkl-567812345678"
    return Labour.plan(
        birthing_person_id=sample_birthing_person.id_,
        first_labour=True,
        due_date=datetime.now(UTC),
        labour_id=labour_id,
    )
