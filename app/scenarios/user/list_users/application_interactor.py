import logging

from app.application.base.interactors import InteractorStrict
from app.application.user.services.authorization import AuthorizationService
from app.application.user.services.user import UserService
from app.domain.user.entity_user import User
from app.domain.user.enums import UserRoleEnum
from app.scenarios.user.list_users.application_payload import (
    ListUsersRequest,
    ListUsersResponse,
    ListUsersResponseElement,
)

log = logging.getLogger(__name__)


class ListUsersInteractor(
    InteractorStrict[ListUsersRequest, ListUsersResponse]
):
    def __init__(
        self,
        authorization_service: AuthorizationService,
        user_service: UserService,
    ):
        self._authorization_service = authorization_service
        self._user_service = user_service

    async def __call__(
        self, request_data: ListUsersRequest
    ) -> ListUsersResponse:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        :raises GatewayError:
        """
        log.info("List users.")
        await self._authorization_service.authorize_and_try_prolong(
            UserRoleEnum.ADMIN
        )

        log.debug("Retrieving list of users.")
        users: list[User] = await self._user_service.get_all(
            request_data.limit, request_data.offset
        )

        response: ListUsersResponse = ListUsersResponse(
            [ListUsersResponseElement.from_user(user) for user in users]
        )

        log.info("List users: response is ready.")
        return response
