import json

import pytest

from app.user.application.dtos.user_summary import UserSummaryDTO
from app.user.domain.entity import User
from app.user.domain.value_objects.user_id import UserId


@pytest.fixture
def user() -> User:
    return User(
        id_=UserId("test"),
        username="test123",
        first_name="User",
        last_name="Name",
        email="test@email.com",
        phone_number="07123123123",
    )


def test_can_convert_to_user_summary_dto(user: User) -> None:
    dto = UserSummaryDTO.from_domain(user)
    assert dto.id == user.id_.value
    assert dto.first_name == user.first_name
    assert dto.last_name == user.last_name


def test_can_convert_user_summary_dto_to_dict(user: User) -> None:
    dto = UserSummaryDTO.from_domain(user)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
