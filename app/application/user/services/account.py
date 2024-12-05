import logging

from app.application.exceptions import AdapterError, GatewayError
from app.application.user.exceptions import AuthenticationError, SessionExpired
from app.application.user.ports.identity_provider import (
    IdentityProviderInterface,
)
from app.application.user.record_session import SessionRecord
from app.application.user.services.authentication import AuthenticationService
from app.application.user.services.session import SessionService
from app.application.user.services.token import TokenService
from app.application.user.services.user import UserService
from app.domain.user.entity_user import User
from app.domain.user.exceptions.non_existence import (
    SessionNotFoundById,
    UserNotFoundById,
)
from app.domain.user.vo_user import UserId, Username

log = logging.getLogger(__name__)


class AccountService:
    def __init__(
        self,
        user_service: UserService,
        authentication_service: AuthenticationService,
        session_service: SessionService,
        token_service: TokenService,
        identity_provider: IdentityProviderInterface,
    ):
        self._user_service = user_service
        self._authentication_service = authentication_service
        self._session_service = session_service
        self._token_service = token_service
        self._identity_provider = identity_provider

    async def sign_up(self, username: Username, password: str) -> None:
        """
        :raises GatewayError:
        :raises UsernameAlreadyExists:
        """
        log.info(f"Started. Username: '{username.value}'.")

        await self._user_service.check_username_uniqueness(username)

        user: User = await self._user_service.create_user(username, password)
        await self._user_service.save_user(user)

        log.info(f"Done. Username: '{username.value}'.")

    async def log_in(self, username: Username, password: str) -> None:
        """
        :raises AuthenticationError:
        :raises GatewayError:
        :raises UserNotFoundByUsername:
        """
        log.info(f"Started. Username: '{username.value}'.")

        if await self._authentication_service.is_authenticated():
            raise AuthenticationError(
                "You are already authenticated. Consider logging out."
            )

        user: User = await self._user_service.get_user_by_username(username)
        self._authentication_service.authenticate(user, password)

        session: SessionRecord = await self._session_service.create_session(
            user.id_
        )
        await self._session_service.save_session(session)

        access_token: str = self._token_service.issue_access_token(session.id_)
        self._token_service.add_access_token_to_request(access_token)

        log.info(
            "Done. User, id: '%s', username '%s', roles '%s'.",
            user.id_.value,
            user.username.value,
            ", ".join(str(role.value) for role in user.roles),
        )

    async def log_out(self) -> None:
        """
        :raises AuthenticationError:
        :raises GatewayError:
        """
        log.info("Started for unknown user.")
        try:
            user_id: UserId = (
                await self._identity_provider.get_current_user_id()
            )
        except (
            AdapterError,
            SessionNotFoundById,
            GatewayError,
            SessionExpired,
        ) as error:
            log.error(f"User id retrieving failed: '{error}'")
            raise AuthenticationError("Not authenticated.") from error

        try:
            user: User = await self._user_service.get_user_by_id(user_id)
        except (
            GatewayError,
            UserNotFoundById,
        ) as error:
            log.error(f"User retrieving failed: '{error}'")
            raise AuthenticationError("Not authenticated.") from error
        log.info(f"User identified. Username: '{user.username.value}'.")

        try:
            session: SessionRecord = (
                await self._identity_provider.get_current_session()
            )
        except (
            AdapterError,
            GatewayError,
            SessionNotFoundById,
            SessionExpired,
        ) as error:
            log.error(f"Session retrieving failed: '{error}'")
            raise AuthenticationError("Not authenticated.") from error

        self._token_service.delete_access_token_from_request()
        log.debug(f"Access token deleted. Session id: '{session.id_}'.")

        try:
            await self._session_service.delete_session(session.id_)
            log.debug(f"Session deleted. Session id: '{session.id_}'.")
        except (
            GatewayError,
            SessionNotFoundById,
        ) as error:
            log.error(f"Session deletion failed: '{error}'")
            raise GatewayError("Session deletion failed.") from error

        log.info(f"Done. Username: '{user.username.value}'.")
