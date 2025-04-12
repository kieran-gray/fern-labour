import logging
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from keycloak import KeycloakOpenID
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.ioc.di_providers.common.settings import PostgresDsn
from app.setup.settings import Settings, SqlaEngineSettings
from app.user.infrastructure.auth.interfaces.controller import AuthController
from app.user.infrastructure.auth.interfaces.service import AuthService
from app.user.infrastructure.auth.keycloak.auth_controller import KeycloakAuthController
from app.user.infrastructure.auth.keycloak.auth_service import KeycloakAuthService

log = logging.getLogger(__name__)


class CommonInfrastructureProvider(Provider):
    component = ComponentEnum.DEFAULT
    scope = Scope.APP

    @provide
    async def provide_async_engine(
        self,
        dsn: PostgresDsn,
        engine_settings: SqlaEngineSettings,
    ) -> AsyncIterable[AsyncEngine]:
        async_engine_params = {
            "url": dsn,
            **engine_settings.model_dump(),
        }
        async_engine = create_async_engine(**async_engine_params)
        log.debug("Async engine created with DSN: %s", dsn)
        yield async_engine
        log.debug("Disposing async engine...")
        await async_engine.dispose()
        log.debug("Engine is disposed.")

    @provide
    def provide_async_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
            info={
                "component": self.component,
            },
        )
        log.debug("Async session maker initialized.")
        return session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        log.debug("Starting async session...")
        async with async_session_maker() as session:
            log.debug("Async session started for '%s'.", self.component)
            yield session
            log.debug("Closing async session.")
        log.debug("Async session closed for '%s'.", self.component)

    @provide
    def provide_auth_client(self, settings: Settings) -> KeycloakOpenID:
        return KeycloakOpenID(
            server_url=settings.security.keycloak.server_url,
            realm_name=settings.security.keycloak.realm,
            client_id=settings.security.keycloak.client_id,
            client_secret_key=settings.security.keycloak.client_secret,
            verify=True,
        )

    @provide
    def provide_auth_service(self, keycloak_openid: KeycloakOpenID) -> AuthService:
        return KeycloakAuthService(keycloak_openid=keycloak_openid)

    @provide
    def provide_auth_controller(self, auth_service: AuthService) -> AuthController:
        return KeycloakAuthController(auth_service=auth_service)
