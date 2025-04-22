from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.labour.domain.contraction.entity import Contraction
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId


@pytest.fixture
def sample_user() -> User:
    user_id = "12345678-1234-5678-1234-567812345678"
    return User(
        id_=UserId(user_id),
        username="test123",
        first_name="User",
        last_name="Name",
        email="test@email.com",
    )


@pytest.fixture
def sample_labour(sample_user: User) -> Labour:
    labour_id = "12345678-abcd-efgh-ijkl-567812345678"
    return Labour.plan(
        birthing_person_id=sample_user.id_,
        first_labour=True,
        due_date=datetime.now(UTC),
        labour_id=labour_id,
    )


def generate_contractions(length: float, intensity: int) -> list[Contraction]:
    contraction_list = []
    last_start_time = None
    for _ in range(5):
        start_time = last_start_time or datetime.now(UTC)
        end_time = start_time + timedelta(minutes=length)

        contraction = Contraction.start(labour_id=LabourId(uuid4()), start_time=start_time)
        contraction.end(end_time=end_time, intensity=intensity)

        contraction_list.append(contraction)
        last_start_time = start_time

    return contraction_list
