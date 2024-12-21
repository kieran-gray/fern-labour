import logging

from dishka import Provider, Scope, from_context, provide
from dishka.dependency_source.composite import CompositeDependencySource

from app.infrastructure.custom_types import AuthScheme, JwtAlgorithm, OAuth2Scheme, PostgresDsn
from app.setup.cookie_params import CookieParams
from app.setup.settings import Settings, SqlaEngineSettings

log = logging.getLogger(__name__)


class SettingsProvider(Provider):
    settings: CompositeDependencySource = from_context(provides=Settings, scope=Scope.RUNTIME)

    @provide(scope=Scope.APP)
    def provide_jwt_algorithm(self, settings: Settings) -> JwtAlgorithm:
        return settings.security.keycloak.jwt_algorithm

    @provide(scope=Scope.APP)
    def provide_keycloak_auth_scheme(self, settings: Settings) -> AuthScheme:
        return AuthScheme(
            server_url=settings.security.keycloak.server_url,
            realm=settings.security.keycloak.realm,
            client_id=settings.security.keycloak.client_id,
            client_secret=settings.security.keycloak.client_secret,
        )

    @provide(scope=Scope.APP)
    def provide_oauth2_scheme(self, settings: Settings) -> OAuth2Scheme:
        base_url = f"{settings.security.keycloak.server_url}"
        realm_url = f"{base_url}/realms/{settings.security.keycloak.realm}"
        protocol_url = f"{realm_url}/protocol/openid-connect"
        return OAuth2Scheme(
            authorizationUrl=f"{protocol_url}/auth",
            tokenUrl=f"{protocol_url}/token",
            refreshUrl=f"{protocol_url}/token",
        )

    @provide(scope=Scope.APP)
    def provide_cookie_params(self, settings: Settings) -> CookieParams:
        is_cookies_secure: bool = settings.security.cookies.secure
        if is_cookies_secure:
            return CookieParams(secure=True, samesite="strict")
        return CookieParams(secure=False)

    @provide(scope=Scope.APP)
    def provide_postgres_dsn(self, settings: Settings) -> PostgresDsn:
        return PostgresDsn(settings.db.postgres.dsn)

    @provide(scope=Scope.APP)
    def provide_sqla_engine_settings(self, settings: Settings) -> SqlaEngineSettings:
        return settings.db.sqla_engine
