import logging

from app.application.base.interactors import InteractorStrict
from app.application.enums import ResponseStatusEnum
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.user import UserService
from app.domain.user.enums import UserRoleEnum
from app.domain.user.vo_user import Username
from app.scenarios.user.base.application_payload import UserResponse
from app.scenarios.user.create_user.application_payload import (
    CreateUserRequest,
)

log = logging.getLogger(__name__)


class CreateUserInteractor(InteractorStrict[CreateUserRequest, UserResponse]):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service

    async def __call__(self, request_data: CreateUserRequest) -> UserResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises UsernameAlreadyExists:
        :raises GatewayError:
        """
        log.info(f"Create user: '{request_data.username}'.")
        await self._authorization_service.authorize_and_try_prolong(
            UserRoleEnum.ADMIN
        )

        username = Username(request_data.username)
        password = request_data.password

        await self._user_service.check_username_uniqueness(username)

        user = await self._user_service.create_user(username, password)
        await self._user_service.assign_roles(user, request_data.roles)

        log.info(
            "New user, id: '%s', username '%s', roles '%s' saved.",
            user.id_,
            username.value,
            ", ".join(str(role.value) for role in user.roles),
        )
        return UserResponse(username.value, ResponseStatusEnum.CREATED)
