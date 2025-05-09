import json

import pytest

from src.user.application.dtos.user import UserDTO
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId


@pytest.fixture
def user() -> User:
    return User(
        id_=UserId("test"),
        username="test123",
        first_name="User",
        last_name="Name",
        email="test@email.com",
        phone_number="+44123123123",
    )


def test_can_convert_to_user_dto(user: User) -> None:
    dto = UserDTO.from_domain(user)
    assert dto.id == user.id_.value
    assert dto.first_name == user.first_name
    assert dto.last_name == user.last_name
    assert dto.email == user.email


def test_can_convert_to_user_summary_dto(user: User) -> None:
    dto = UserDTO.from_domain(user)
    summary_dto = dto.to_summary()
    assert dto.id == summary_dto.id
    assert dto.first_name == summary_dto.first_name
    assert dto.last_name == summary_dto.last_name


def test_can_convert_user_dto_to_dict(user: User) -> None:
    dto = UserDTO.from_domain(user)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
