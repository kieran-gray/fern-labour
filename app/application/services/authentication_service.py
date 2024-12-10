import logging

from app.application.adapters.identity_provider import IdentityProvider
from app.application.adapters.password_hasher import PasswordHasher
from app.application.exceptions import AuthenticationError, SessionExpired, AdapterError
from app.domain.entities.user import User
from app.domain.exceptions.user_session import SessionNotFoundById

log = logging.getLogger(__name__)


class AuthenticationService:
    def __init__(self, password_hasher: PasswordHasher, identity_provider: IdentityProvider):
        self._password_hasher = password_hasher
        self._identity_provider = identity_provider

    def authenticate(self, user: User, password: str) -> None:
        """
        :raises AuthenticationError:
        """

        if not user.is_active:
            raise AuthenticationError("Your account has been deactivated. Please contact support.")

        if not self._password_hasher.verify(
            raw_password=password,
            hashed_password=user.password_hash.value,
        ):
            raise AuthenticationError("Wrong password.")

    async def is_authenticated(self) -> bool:
        try:
            await self._identity_provider.get_current_user_id()
        except (SessionNotFoundById, SessionExpired, AdapterError) as error:
            log.error(f"Authentication failed: '{error}'")
            return False
        return True
