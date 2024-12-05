# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.application.user.gateways.session import SessionGatewayInterface
from app.application.user.gateways.user import UserGatewayInterface
from app.application.user.ports.access_token_processor import (
    AccessTokenProcessorInterface,
)
from app.application.user.ports.identity_provider import (
    IdentityProviderInterface,
)
from app.application.user.ports.password_hasher import PasswordHasherInterface
from app.application.user.ports.session_id_generator import (
    SessionIdGeneratorInterface,
)
from app.application.user.ports.session_timer import SessionTimerInterface
from app.application.user.ports.user_id_generator import (
    UserIdGeneratorInterface,
)
from app.infrastructure.user.adapters.access_token_processor_jwt import (
    JwtAccessTokenProcessor,
)
from app.infrastructure.user.adapters.identity_provider_jwt import (
    JwtIdentityProvider,
)
from app.infrastructure.user.adapters.password_hasher_bcrypt import (
    BcryptPasswordHasher,
)
from app.infrastructure.user.adapters.session_id_generator_str import (
    StrSessionIdGenerator,
)
from app.infrastructure.user.adapters.session_timer_utc import UtcSessionTimer
from app.infrastructure.user.adapters.user_id_generator_uuid import (
    UuidUserIdGenerator,
)
from app.infrastructure.user.gateways_impl_sqla.session import (
    SqlaSessionGateway,
)
from app.infrastructure.user.gateways_impl_sqla.user import SqlaUserGateway


class UserGatewaysProvider(Provider):
    session_gateway = provide(
        source=SqlaSessionGateway,
        scope=Scope.REQUEST,
        provides=SessionGatewayInterface,
    )

    user_gateway = provide(
        source=SqlaUserGateway,
        scope=Scope.REQUEST,
        provides=UserGatewayInterface,
    )


class UserAdaptersProvider(Provider):
    access_token_processor = provide(
        source=JwtAccessTokenProcessor,
        scope=Scope.REQUEST,
        provides=AccessTokenProcessorInterface,
    )
    identity_provider = provide(
        source=JwtIdentityProvider,
        scope=Scope.REQUEST,
        provides=IdentityProviderInterface,
    )
    password_hasher = provide(
        source=BcryptPasswordHasher,
        scope=Scope.APP,
        provides=PasswordHasherInterface,
    )
    session_id_generator = provide(
        source=StrSessionIdGenerator,
        scope=Scope.APP,
        provides=SessionIdGeneratorInterface,
    )
    session_timer = provide(
        source=UtcSessionTimer,
        scope=Scope.APP,
        provides=SessionTimerInterface,
    )
    user_id_generator = provide(
        source=UuidUserIdGenerator,
        scope=Scope.APP,
        provides=UserIdGeneratorInterface,
    )
