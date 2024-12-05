import logging

from app.application.exceptions import AdapterError, GatewayError
from app.application.user.exceptions import (
    AuthenticationError,
    AuthorizationError,
    SessionExpired,
)
from app.application.user.ports.identity_provider import (
    IdentityProviderInterface,
)
from app.application.user.record_session import SessionRecord
from app.application.user.services.authentication import AuthenticationService
from app.application.user.services.session import SessionService
from app.application.user.services.token import TokenService
from app.domain.user.enums import UserRoleEnum
from app.domain.user.exceptions.non_existence import (
    SessionNotFoundById,
    UserNotFoundById,
)
from app.domain.user.vo_user import UserId

log = logging.getLogger(__name__)


class AuthorizationService:
    def __init__(
        self,
        authentication_service: AuthenticationService,
        identity_provider: IdentityProviderInterface,
        session_service: SessionService,
        token_service: TokenService,
    ):
        self._authentication_service = authentication_service
        self._identity_provider = identity_provider
        self._session_service = session_service
        self._token_service = token_service

    async def get_current_user_id(self) -> UserId:
        log.debug("Check authorization: started.")

        if not await self._authentication_service.is_authenticated():
            raise AuthenticationError("Not authenticated.")

        try:
            current_user_id: UserId = (
                await self._identity_provider.get_current_user_id()
            )
        except (
            AdapterError,
            GatewayError,
            SessionNotFoundById,
            SessionExpired,
            UserNotFoundById,
        ) as error:
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
        except (
            AdapterError,
            GatewayError,
            SessionNotFoundById,
            SessionExpired,
            UserNotFoundById,
        ) as error:
            log.error("Getting user roles failed: '{error}'.")
            raise AuthorizationError("Authorization failed.") from error

        if role_required not in current_user_roles:
            log.error(
                "Authorization failed. Roles: %s, Required: %s",
                current_user_roles,
                role_required,
            )
            raise AuthorizationError("Not authorized.")

    async def authorize_and_try_prolong(
        self, role_required: UserRoleEnum
    ) -> None:
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
            session: SessionRecord = (
                await self._identity_provider.get_current_session()
            )

            await self._session_service.prolong_session(session)
            log.debug(f"Prolonged session id: {session.id_}")

            new_access_token: str = self._token_service.issue_access_token(
                session.id_
            )
            self._token_service.add_access_token_to_request(new_access_token)
            log.debug(f"New access token for session id: {session.id_}")

        except (
            AdapterError,
            GatewayError,
            SessionNotFoundById,
            SessionExpired,
        ) as error:
            log.error(f"Prolongation failed: '{error}'.")
