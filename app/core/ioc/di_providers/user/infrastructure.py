from dishka import Provider, Scope, provide

from app.application.adapters.auth_provider import AuthProvider
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.infrastructure.adapters.auth_provider_keycloak import KeycloakAuthProvider
from app.infrastructure.persistence.repositories.user_repository import SQLAlchemyUserRepository


class UserRepositoriesProvider(Provider):
    user_repository = provide(
        source=SQLAlchemyUserRepository,
        scope=Scope.REQUEST,
        provides=BirthingPersonRepository,
    )


class UserAdaptersProvider(Provider):
    auth_provider = provide(
        source=KeycloakAuthProvider,
        scope=Scope.APP,
        provides=AuthProvider,
    )
