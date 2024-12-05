import logging

from app.application.exceptions import AdapterError, GatewayError
from app.application.user.exceptions import AuthenticationError, SessionExpired
from app.application.user.ports.identity_provider import (
    IdentityProviderInterface,
)
from app.application.user.ports.password_hasher import PasswordHasherInterface
from app.domain.user.entity_user import User
from app.domain.user.exceptions.non_existence import SessionNotFoundById

log = logging.getLogger(__name__)


class AuthenticationService:
    def __init__(
        self,
        password_hasher: PasswordHasherInterface,
        identity_provider: IdentityProviderInterface,
    ):
        self._password_hasher = password_hasher
        self._identity_provider = identity_provider

    def authenticate(self, user: User, password: str) -> None:
        """
        :raises AuthenticationError:
        """

        if not user.is_active:
            raise AuthenticationError(
                "Your account has been deactivated. Please contact support."
            )

        if not self._password_hasher.verify(
            raw_password=password,
            hashed_password=user.password_hash.value,
        ):
            raise AuthenticationError("Wrong password.")

    async def is_authenticated(self) -> bool:
        try:
            await self._identity_provider.get_current_user_id()
        except (
            AdapterError,
            SessionNotFoundById,
            GatewayError,
            SessionExpired,
        ) as error:
            log.error(f"Authentication failed: '{error}'")
            return False

        return True
