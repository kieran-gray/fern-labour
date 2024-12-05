import logging

from app.application.base.interactors import InteractorStrict
from app.application.enums import ResponseStatusEnum
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.session import SessionService
from app.application.user.services.user import UserService
from app.domain.user.enums import UserRoleEnum
from app.domain.user.vo_user import Username
from app.scenarios.user.base.application_payload import UserResponse
from app.scenarios.user.deactivate_user.application_payload import (
    DeactivateUserRequest,
)

log = logging.getLogger(__name__)


class DeactivateUserInteractor(
    InteractorStrict[DeactivateUserRequest, UserResponse]
):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
        session_service: SessionService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service
        self._session_service = session_service

    async def __call__(
        self, request_data: DeactivateUserRequest
    ) -> UserResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises UserNotFoundByUsername:
        :raises GatewayError:
        """
        log.info(f"Deactivate user: '{request_data.username}'.")
        await self._authorization_service.authorize_and_try_prolong(
            UserRoleEnum.ADMIN
        )

        username = Username(request_data.username)
        user = await self._user_service.get_user_by_username(username)

        user.deactivate()
        await self._user_service.save_user(user)

        await self._session_service.delete_all_sessions_by_user_id(user.id_)

        log.info(
            f"User '{request_data.username}' deactivated.",
        )
        return UserResponse(request_data.username, ResponseStatusEnum.UPDATED)
