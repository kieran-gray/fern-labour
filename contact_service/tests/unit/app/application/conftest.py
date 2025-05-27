from unittest.mock import AsyncMock

import pytest_asyncio

from src.application.contact_message_query_service import ContactMessageQueryService
from src.application.contact_message_service import ContactMessageService
from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage
from src.domain.repository import ContactMessageRepository
from src.infrastructure.log_alert_service import LogAlertService
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


class MockContactMessageRepository(ContactMessageRepository):
    _data = {}

    async def save(self, contact_message: ContactMessage) -> None:
        self._data[contact_message.id_.value] = contact_message

    async def delete(self, contact_message: ContactMessage) -> None:
        self._data.pop(contact_message.id_.value)

    async def get_by_id(self, contact_message_id: ContactMessageId) -> ContactMessage | None:
        return self._data.get(contact_message_id.value, None)

    async def get_by_ids(self, contact_message_ids: list[ContactMessageId]) -> list[ContactMessage]:
        contact_messages = []
        for contact_message_id in contact_message_ids:
            if contact_message := self._data.get(contact_message_id.value, None):
                contact_messages.append(contact_message)
        return contact_messages


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)


@pytest_asyncio.fixture
async def contact_message_repo() -> ContactMessageRepository:
    repo = MockContactMessageRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def contact_message_service(
    contact_message_repo: ContactMessageRepository,
) -> ContactMessageService:
    return ContactMessageService(
        contact_message_repository=contact_message_repo,
        event_producer=AsyncMock(),
        alert_service=LogAlertService(),
    )


@pytest_asyncio.fixture
async def contact_message_query_service(
    contact_message_repo: ContactMessageRepository,
) -> ContactMessageQueryService:
    return ContactMessageQueryService(contact_message_repository=contact_message_repo)
