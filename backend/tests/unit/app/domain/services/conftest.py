from datetime import UTC, datetime

import pytest

from app.domain.labour.entity import Labour
from app.domain.user.entity import User
from app.domain.user.vo_user_id import UserId


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
