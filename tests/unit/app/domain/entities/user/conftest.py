from uuid import UUID

import pytest

from app.domain.entities.user import User


@pytest.fixture
def sample_user() -> User:
    user_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    username: str = "username@example.com"
    password_hash: bytes = bytes.fromhex("123456789abcdef0")
    return User.create(
        user_id=user_id, username=username, password_hash=password_hash
    )
