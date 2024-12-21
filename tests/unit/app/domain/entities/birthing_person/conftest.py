from uuid import UUID

import pytest

from app.domain.birthing_person.entity import BirthingPerson


@pytest.fixture
def sample_birthing_person() -> BirthingPerson:
    user_id = "12345678-1234-5678-1234-567812345678"
    return BirthingPerson.create(user_id=user_id, name="User Name", first_labour=True)
