# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.application.adapters.access_token_processor import AccessTokenProcessor
from app.application.adapters.identity_provider import IdentityProvider
from app.application.adapters.password_hasher import PasswordHasher
from app.application.adapters.session_timer import SessionTimer
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.adapters.access_token_processor_jwt import JwtAccessTokenProcessor
from app.infrastructure.adapters.identity_provider_jwt import JwtIdentityProvider
from app.infrastructure.adapters.password_hasher_bcrypt import BcryptPasswordHasher
from app.infrastructure.adapters.session_timer_utc import UtcSessionTimer
from app.infrastructure.persistence.repositories.user_repository import SQLAlchemyUserRepository


class UserRepositoriesProvider(Provider):
    user_repository = provide(
        source=SQLAlchemyUserRepository,
        scope=Scope.REQUEST,
        provides=UserRepository,
    )


class UserAdaptersProvider(Provider):
    access_token_processor = provide(
        source=JwtAccessTokenProcessor,
        scope=Scope.REQUEST,
        provides=AccessTokenProcessor,
    )
    identity_provider = provide(
        source=JwtIdentityProvider,
        scope=Scope.REQUEST,
        provides=IdentityProvider,
    )
    password_hasher = provide(
        source=BcryptPasswordHasher,
        scope=Scope.APP,
        provides=PasswordHasher,
    )
    session_timer = provide(
        source=UtcSessionTimer,
        scope=Scope.APP,
        provides=SessionTimer,
    )
