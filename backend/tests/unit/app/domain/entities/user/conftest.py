import pytest

from app.domain.user.entity import User


@pytest.fixture
def sample_user() -> User:
    user_id = "12345678-1234-5678-1234-567812345678"
    return User(user_id=user_id, first_name="User", last_name="Name", email="test@email.com")
