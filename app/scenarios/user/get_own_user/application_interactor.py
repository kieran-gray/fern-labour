import logging

from app.application.base.interactors import InteractorFlexible
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.user import UserService
from app.domain.user.entity_user import User
from app.scenarios.user.get_own_user.application_payload import (
    GetOwnUserResponse,
)

log = logging.getLogger(__name__)


class GetOwnUserInteractor(InteractorFlexible):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service

    async def __call__(self) -> GetOwnUserResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises GatewayError:
        """
        log.info("Get own user id")
        user_id = await self._authorization_service.get_current_user_id()

        log.debug("Retrieving own user.")
        user: User = await self._user_service.get_user_by_id(user_id=user_id)

        response = GetOwnUserResponse(user.username.value, user.roles)

        log.info("Own user: response is ready.")
        return response
