import logging

from app.application.adapters.identity_provider import IdentityProvider
from app.application.exceptions import AuthenticationError, AuthorizationError, SessionExpired
from app.application.services.authentication_service import AuthenticationService
from app.application.services.token_service import TokenService
from app.application.services.user_session_service import UserSessionService
from app.domain.entities.user import UserRoleEnum
from app.domain.exceptions.user import UserNotFoundById
from app.domain.exceptions.user_session import SessionNotFoundById
from app.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class AuthorizationService:
    def __init__(
        self,
        authentication_service: AuthenticationService,
        identity_provider: IdentityProvider,
        user_session_service: UserSessionService,
        token_service: TokenService,
    ):
        self._authentication_service = authentication_service
        self._identity_provider = identity_provider
        self._user_session_service = user_session_service
        self._token_service = token_service

    async def get_current_user_id(self) -> UserId:
        log.debug("Check authorization: started.")

        if not await self._authentication_service.is_authenticated():
            raise AuthenticationError("Not authenticated.")

        try:
            current_user_id: UserId = await self._identity_provider.get_current_user_id()
        except (SessionNotFoundById, SessionExpired, UserNotFoundById) as error:
            log.error(f"Getting user id failed: '{error}'.")
            raise AuthorizationError("Authorization failed.") from error
        return current_user_id

    async def check_authorization(self, role_required: UserRoleEnum) -> None:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        """

        if not await self._authentication_service.is_authenticated():
            raise AuthenticationError("Not authenticated.")

        try:
            current_user_roles: set[
                UserRoleEnum
            ] = await self._identity_provider.get_current_user_roles()
        except (SessionNotFoundById, SessionExpired, UserNotFoundById) as error:
            log.error("Getting user roles failed: '{error}'.")
            raise AuthorizationError("Authorization failed.") from error

        if role_required not in current_user_roles:
            log.error(
                "Authorization failed. Roles: %s, Required: %s",
                current_user_roles,
                role_required,
            )
            raise AuthorizationError("Not authorized.")

    async def authorize_and_try_prolong(self, role_required: UserRoleEnum) -> None:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        """

        await self.check_authorization(role_required)
        await self._try_prolong_session()

        log.debug("Authorize and prolong: done.")

    async def _try_prolong_session(self) -> None:
        log.debug("Try prolong session: started.")

        try:
            user_id = await self.get_current_user_id()
            user_session = await self._user_session_service.prolong_user_session(user_id=user_id)
            log.debug(f"Prolonged session for user: {user_id.value}")

            new_access_token: str = self._token_service.issue_access_token(user_id.value, user_session.id_)
            self._token_service.add_access_token_to_request(new_access_token)
            log.debug(f"New access token for session id: {user_session.id_}")

        except (
            AuthorizationError,
            AuthenticationError,
            SessionNotFoundById,
            SessionExpired,
        ) as error:
            log.error(f"Prolongation failed: '{error}'.")
