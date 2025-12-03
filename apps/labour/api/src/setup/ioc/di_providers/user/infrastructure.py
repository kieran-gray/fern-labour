from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from keycloak import KeycloakAdmin

from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
from src.user.domain.repository import UserRepository
from src.user.infrastructure.persistence.repositories.user_repository import KeycloakUserRepository


class UserInfrastructureProvider(Provider):
    component = ComponentEnum.USER
    scope = Scope.APP

    @provide
    def provide_admin_client(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> KeycloakAdmin:
        return KeycloakAdmin(
            server_url=settings.security.keycloak.server_url,
            realm_name=settings.security.keycloak.realm,
            client_id=settings.security.user_management.client_id,
            client_secret_key=settings.security.user_management.client_secret,
            verify=True,
        )

    @provide
    def provide_user_repository(self, keycloak_admin: KeycloakAdmin) -> UserRepository:
        return KeycloakUserRepository(keycloak_admin=keycloak_admin)
