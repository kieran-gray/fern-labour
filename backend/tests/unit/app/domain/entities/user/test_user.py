from app.user.domain.entity import User
from app.user.domain.value_objects.user_id import UserId


def test_user_init():
    User(
        id_=UserId("12345678-1234-5678-1234-567812345678"),
        username="test123",
        first_name="test",
        last_name="test",
        email="test@email.com",
    )
