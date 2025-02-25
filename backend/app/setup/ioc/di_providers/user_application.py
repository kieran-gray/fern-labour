from dishka import Provider, Scope, provide

from app.application.services.user_service import UserService
from app.domain.user.repository import UserRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class UserApplicationProvider(Provider):
    component = ComponentEnum.USER
    scope = Scope.REQUEST

    @provide
    def provide_user_service(self, user_repository: UserRepository) -> UserService:
        return UserService(user_repository=user_repository)
