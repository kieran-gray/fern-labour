from dishka import Provider, Scope, provide
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings
from keycloak import KeycloakOpenID  # type: ignore


class CommonPresentationProvider(Provider):
    component = ComponentEnum.DEFAULT
    scope = Scope.APP

    @provide
    def provide_auth_client(self, settings: Settings) -> KeycloakOpenID:
        return KeycloakOpenID(
            server_url=settings.security.keycloak.docker_url,
            realm_name=settings.security.keycloak.realm,
            client_id=settings.security.keycloak.client_id,
            client_secret_key=settings.security.keycloak.client_secret,
            verify=True,
        )

    @provide
    def provide_oauth2_code_bearer(self, settings: Settings) -> KeycloakOpenID:
        keycloak_settings = settings.security.keycloak
        base_url = f"{keycloak_settings.server_url}/realms/{keycloak_settings.realm}"
        oidc_url = f"{base_url}/protocol/openid-connect"
        token_url = f"{oidc_url}/token"
        return OAuth2AuthorizationCodeBearer(
            authorizationUrl=f"{oidc_url}/auth",
            tokenUrl=token_url,
            refreshUrl=token_url,
        )
