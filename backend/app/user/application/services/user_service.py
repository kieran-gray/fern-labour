from app.user.application.dtos.user import UserDTO
from app.user.application.dtos.user_summary import UserSummaryDTO
from app.user.domain.exceptions import UserNotFoundById
from app.user.domain.repository import UserRepository
from app.user.domain.value_objects.user_id import UserId


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def get(self, user_id: str) -> UserDTO:
        domain_id = UserId(user_id)
        user = await self._user_repository.get_by_id(domain_id)
        if not user:
            raise UserNotFoundById(user_id=user_id)

        return UserDTO.from_domain(user)

    async def get_many(self, user_ids: list[str]) -> list[UserDTO]:
        domain_ids = [UserId(user_id) for user_id in user_ids]
        users = await self._user_repository.get_by_ids(domain_ids)
        # TODO handle missing
        return [UserDTO.from_domain(user) for user in users]

    async def get_summary(self, user_id: str) -> UserSummaryDTO:
        domain_id = UserId(user_id)
        user = await self._user_repository.get_by_id(domain_id)
        if not user:
            raise UserNotFoundById(user_id=user_id)

        return UserSummaryDTO.from_domain(user)

    async def get_many_summary(self, user_ids: list[str]) -> list[UserSummaryDTO]:
        domain_ids = [UserId(user_id) for user_id in user_ids]
        users = await self._user_repository.get_by_ids(domain_ids)
        # TODO handle missing
        return [UserSummaryDTO.from_domain(user) for user in users]
