import pytest

from app.application.dtos.user import UserDTO
from app.application.dtos.user_summary import UserSummaryDTO
from app.application.services.user_service import UserService
from app.domain.user.entity import User
from app.domain.user.exceptions import (
    UserNotFoundById,
)
from app.domain.user.vo_user_id import UserId


async def register(user_service: UserService, ids: list[str]):
    for id in ids:
        await user_service._user_repository.save(
            User(
                id_=UserId(id),
                username="test",
                email="test@email.com",
                first_name="User",
                last_name="Name",
            )
        )


async def test_get_user(user_service: UserService):
    user_id = "test"
    await register(user_service, [user_id])
    user = await user_service.get(user_id)

    assert isinstance(user, UserDTO)
    assert user.first_name == "User"
    assert user.last_name == "Name"


async def test_get_many_users(user_service: UserService):
    ids = ["test1", "test2", "test3"]
    await register(user_service, ids)
    users = await user_service.get_many(ids)

    assert len(users) == 3


async def test_cannot_get_non_existent_user(
    user_service: UserService,
):
    with pytest.raises(UserNotFoundById):
        await user_service.get("test")


async def test_get_user_summary(user_service: UserService):
    user_id = "test"
    await register(user_service, [user_id])
    user = await user_service.get_summary(user_id)

    assert isinstance(user, UserSummaryDTO)
    assert user.first_name == "User"
    assert user.last_name == "Name"


async def test_get_many_user_summaries(user_service: UserService):
    ids = ["test1", "test2", "test3"]
    await register(user_service, ids)
    users = await user_service.get_many_summary(ids)

    assert len(users) == 3


async def test_get_many_users_returns_empty_list_for_non_existent_ids(
    user_service: UserService,
) -> None:
    users = await user_service.get_many(["Test", "ABC"])
    assert len(users) == 0
    assert isinstance(users, list)


async def test_cannot_get_summary_for_non_existent_user(
    user_service: UserService,
):
    with pytest.raises(UserNotFoundById):
        await user_service.get_summary("test")
