import logging

from app.application.base.interactors import InteractorStrict
from app.application.enums import ResponseStatusEnum
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.user import UserService
from app.domain.user.enums import UserRoleEnum
from app.domain.user.vo_user import Username
from app.scenarios.user.base.application_payload import UserResponse
from app.scenarios.user.grant_admin.application_payload import (
    GrantAdminRequest,
)

log = logging.getLogger(__name__)


class GrantAdminInteractor(InteractorStrict[GrantAdminRequest, UserResponse]):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service

    async def __call__(self, request_data: GrantAdminRequest) -> UserResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises UserNotFoundByUsername:
        :raises GatewayError:
        """
        log.info(f"Granting admin to user: '{request_data.username}'.")
        await self._authorization_service.authorize_and_try_prolong(
            UserRoleEnum.ADMIN
        )

        username = Username(request_data.username)
        user = await self._user_service.get_user_by_username(username)

        user.grant_admin()
        await self._user_service.save_user(user)

        log.info(f"User '{username.value}' is promoted to admin.")
        return UserResponse(username.value, ResponseStatusEnum.UPDATED)
