import logging

from app.application.adapters.identity_provider import IdentityProvider
from app.application.exceptions import AuthenticationError, SessionExpired
from app.application.services.authentication_service import AuthenticationService
from app.application.services.token_service import TokenService
from app.application.services.user_service import UserService
from app.application.services.user_session_service import UserSessionService
from app.domain.entities.user import User
from app.domain.entities.user_session import UserSession
from app.domain.exceptions.user import UserNotFoundById
from app.domain.exceptions.user_session import SessionNotFoundById
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.user_username import Username

log = logging.getLogger(__name__)


class AccountService:
    def __init__(
        self,
        user_service: UserService,
        authentication_service: AuthenticationService,
        user_session_service: UserSessionService,
        token_service: TokenService,
        identity_provider: IdentityProvider,
    ):
        self._user_service = user_service
        self._authentication_service = authentication_service
        self._user_session_service = user_session_service
        self._token_service = token_service
        self._identity_provider = identity_provider

    async def sign_up(self, username: str, password: str) -> None:
        log.info(f"Started. Username: '{username}'.")
        username = Username(username)
        await self._user_service.check_username_uniqueness(username.value)

        user: User = await self._user_service.create_user(username, password)
        await self._user_service.save_user(user)

        log.info(f"Done. Username: '{username.value}'.")

    async def log_in(self, username: str, password: str) -> None:
        log.info(f"Started. Username: '{username}'.")

        username = Username(username)
        if await self._authentication_service.is_authenticated():
            raise AuthenticationError("You are already authenticated. Consider logging out.")

        user: User = await self._user_service.get_user_by_username(username)
        self._authentication_service.authenticate(user, password)

        session: UserSession = await self._user_session_service.create_user_session(user.id_)

        access_token: str = self._token_service.issue_access_token(user.id_.value, session.id_)
        self._token_service.add_access_token_to_request(access_token)

        log.info(
            "Done. User, id: '%s', username '%s', roles '%s'.",
            user.id_.value,
            user.username.value,
            ", ".join(str(role.value) for role in user.roles),
        )

    async def log_out(self) -> None:
        log.info("Started for unknown user.")
        try:
            user_id: UserId = await self._identity_provider.get_current_user_id()
        except (SessionNotFoundById, SessionExpired) as error:
            log.error(f"User id retrieving failed: '{error}'")
            raise AuthenticationError("Not authenticated.") from error

        try:
            user: User = await self._user_service.get_user_by_id(user_id)
        except UserNotFoundById as error:
            log.error(f"User retrieving failed: '{error}'")
            raise AuthenticationError("Not authenticated.") from error
        log.info(f"User identified. Username: '{user.username.value}'.")

        if not user.session:
            raise AuthenticationError("Not authenticated.")

        self._token_service.delete_access_token_from_request()

        user.delete_all_sessions()
        self._user_service.save_user(user)

        log.info(f"Done. Username: '{user.username.value}'.")
