import pytest

from src.user.application.dtos.user import UserDTO


@pytest.fixture
def user_dto() -> UserDTO:
    data_dict = {
        "id": "test",
        "username": "user_name_1",
        "first_name": "name",
        "last_name": "LastName",
        "email": "test@email.com",
        "phone_number": "123",
    }
    return UserDTO(**data_dict)


def test_can_serialize_user_dto():
    data_dict = {
        "id": "test",
        "username": "user_name_1",
        "first_name": "name",
        "last_name": "LastName",
        "email": "test@email.com",
        "phone_number": "123",
    }
    dto = UserDTO(**data_dict)
    assert dto.to_dict() == data_dict


def test_can_get_destinations(user_dto: UserDTO):
    assert user_dto.destination("sms") == user_dto.phone_number
    assert user_dto.destination("email") == user_dto.email
