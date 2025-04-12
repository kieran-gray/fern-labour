from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from keycloak import KeycloakAdmin

from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings
from app.user.domain.repository import UserRepository
from app.user.infrastructure.persistence.repositories.user_repository import KeycloakUserRepository


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
            username=settings.security.keycloak.admin_username,
            password=settings.security.keycloak.admin_password,
            client_id="admin-cli",
            verify=True,
        )

    @provide
    def provide_user_repository(self, keycloak_admin: KeycloakAdmin) -> UserRepository:
        return KeycloakUserRepository(keycloak_admin=keycloak_admin)
