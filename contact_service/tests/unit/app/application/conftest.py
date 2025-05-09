import pytest
import pytest_asyncio
from fakeredis import FakeValkey

from src.infrastructure.security.rate_limiting.interface import RateLimiter
from src.infrastructure.security.rate_limiting.redis import RedisRateLimiter
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.repository import UserRepository
from src.user.domain.value_objects.user_id import UserId


class MockUserRepository(UserRepository):
    _data = {}

    async def save(self, user: User) -> None:
        self._data[user.id_.value] = user

    async def delete(self, user: User) -> None:
        self._data.pop(user.id_.value)

    async def get_by_id(self, user_id: UserId) -> User | None:
        return self._data.get(user_id.value, None)

    async def get_by_ids(self, user_ids: list[UserId]) -> list[User]:
        users = []
        for user_id in user_ids:
            if user := self._data.get(user_id.value, None):
                users.append(user)
        return users


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest.fixture
def rate_limiter() -> RateLimiter:
    return RedisRateLimiter(redis=FakeValkey())


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)
