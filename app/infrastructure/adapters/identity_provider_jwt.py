from uuid import UUID

from app.application.adapters.access_token_processor import AccessTokenProcessor
from app.application.adapters.access_token_request_handler import AccessTokenRequestHandler
from app.application.adapters.identity_provider import IdentityProvider
from app.application.adapters.session_timer import SessionTimer
from app.application.exceptions import SessionExpired
from app.application.services.user_service import UserService
from app.domain.entities.user import User, UserRoleEnum
from app.domain.entities.user_session import UserSession
from app.domain.exceptions.user import UserNotFoundById
from app.domain.exceptions.user_session import SessionNotFoundById
from app.domain.value_objects.user_id import UserId


class JwtIdentityProvider(IdentityProvider):
    def __init__(
        self,
        access_token_handler: AccessTokenRequestHandler,
        token_processor: AccessTokenProcessor,
        session_timer: SessionTimer,
        user_service: UserService,
    ):
        self._access_token_handler = access_token_handler
        self._token_processor = token_processor
        self._session_timer = session_timer
        self._user_service = user_service

    async def get_current_user(self) -> User:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """
        access_token: str = self._access_token_handler.get_access_token_from_request()
        user_id, _ = self._token_processor.extract_ids(access_token)

        user = await self._user_service.get_user_by_id(UserId(UUID(user_id)))  # TODO don't like it
        if user is None:
            raise UserNotFoundById(user_id)

        return user

    async def get_current_session(self) -> UserSession:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """
        access_token: str = self._access_token_handler.get_access_token_from_request()
        user_id, session_id = self._token_processor.extract_ids(access_token)

        user = await self._user_service.get_user_by_id(UserId(UUID(user_id)))  # TODO don't like it
        if user is None:
            raise UserNotFoundById(user_id)

        if user.session.id_ != UUID(session_id):
            raise SessionNotFoundById(session_id)

        if user.session.expiration <= self._session_timer.current_time:
            raise SessionExpired(session_id)

        return user.session

    async def get_current_user_id(self) -> UserId:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """
        user: User = await self.get_current_user()

        return user.id_

    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        :raises UserNotFoundById:
        """
        user: User = await self.get_current_user()

        return user.roles
