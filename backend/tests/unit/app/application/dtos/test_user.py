import json

import pytest

from app.application.dtos.user import UserDTO
from app.domain.user.entity import User
from app.domain.user.vo_user_id import UserId
from app.labour.domain.subscription.enums import ContactMethod


@pytest.fixture
def user() -> User:
    return User(
        id_=UserId("test"),
        username="test123",
        first_name="User",
        last_name="Name",
        email="test@email.com",
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


def test_user_destination(user: User) -> None:
    dto = UserDTO.from_domain(user)
    assert dto.destination(ContactMethod.SMS.value) == user.phone_number
    assert dto.destination(ContactMethod.EMAIL.value) == user.email


def test_user_destination_returns_none(user: User) -> None:
    dto = UserDTO.from_domain(user)
    dto.email = None
    dto.phone_number = None
    assert dto.destination(ContactMethod.SMS.value) is None
    assert dto.destination(ContactMethod.EMAIL.value) is None


def test_user_destination_invalid_contact_method(user: User) -> None:
    dto = UserDTO.from_domain(user)
    with pytest.raises(ValueError):
        dto.destination("test")
