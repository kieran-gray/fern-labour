import logging

from app.application.base.interactors import InteractorFlexible
from app.application.enums import ResponseStatusEnum
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.session import SessionService
from app.application.user.services.user import UserService
from app.scenarios.user.delete_own_user.application_payload import (
    DeleteOwnUserResponse,
)

log = logging.getLogger(__name__)


class DeleteOwnUserInteractor(InteractorFlexible):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
        session_service: SessionService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service
        self._session_service = session_service

    async def __call__(self) -> DeleteOwnUserResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises GatewayError:
        :raises UserNotFoundById:
        """
        log.info("Get own user id")
        user_id = await self._authorization_service.get_current_user_id()

        log.debug("Deleting own user.")
        await self._user_service.delete_user_by_id(user_id=user_id)

        log.debug("Deleting all sessions for user.")
        await self._session_service.delete_all_sessions_by_user_id(user_id)

        response = DeleteOwnUserResponse(status=ResponseStatusEnum.DELETED)

        log.info("Delete own user: response is ready.")
        return response
