from app.application.user.exceptions import SessionExpired
from app.application.user.gateways.session import SessionGatewayInterface
from app.application.user.gateways.user import UserGatewayInterface
from app.application.user.ports.access_token_processor import (
    AccessTokenProcessorInterface,
)
from app.application.user.ports.access_token_request_handler import (
    AccessTokenRequestHandlerInterface,
)
from app.application.user.ports.identity_provider import (
    IdentityProviderInterface,
)
from app.application.user.ports.session_timer import SessionTimerInterface
from app.application.user.record_session import SessionRecord
from app.domain.user.entity_user import User
from app.domain.user.enums import UserRoleEnum
from app.domain.user.exceptions.non_existence import (
    SessionNotFoundById,
    UserNotFoundById,
)
from app.domain.user.vo_user import UserId


class JwtIdentityProvider(IdentityProviderInterface):
    def __init__(
        self,
        access_token_handler: AccessTokenRequestHandlerInterface,
        token_processor: AccessTokenProcessorInterface,
        session_timer: SessionTimerInterface,
        session_gateway: SessionGatewayInterface,
        user_gateway: UserGatewayInterface,
    ):
        self._access_token_handler = access_token_handler
        self._token_processor = token_processor
        self._session_timer = session_timer
        self._session_gateway = session_gateway
        self._user_gateway = user_gateway

    async def get_current_session(self) -> SessionRecord:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """
        access_token: str = (
            self._access_token_handler.get_access_token_from_request()
        )
        session_id: str = self._token_processor.extract_session_id(
            access_token
        )

        session: SessionRecord | None = await self._session_gateway.read(
            session_id
        )
        if session is None:
            raise SessionNotFoundById(session_id)

        if session.expiration <= self._session_timer.current_time:
            raise SessionExpired(session_id)

        return session

    async def get_current_user_id(self) -> UserId:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """
        session: SessionRecord = await self.get_current_session()

        return session.user_id

    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        :raises UserNotFoundById:
        """
        user_id: UserId = await self.get_current_user_id()
        user: User | None = await self._user_gateway.read_by_id(user_id)

        if user is None:
            raise UserNotFoundById(user_id)

        return user.roles
