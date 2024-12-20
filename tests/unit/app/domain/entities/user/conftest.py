from uuid import UUID

import pytest

from app.domain.birthing_person.entity import BirthingPerson


@pytest.fixture
def sample_user() -> BirthingPerson:
    user_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    username: str = "username@example.com"
    password_hash: bytes = bytes.fromhex("123456789abcdef0")
    return BirthingPerson.create(
        user_id=user_id, username=username, password_hash=password_hash
    )
