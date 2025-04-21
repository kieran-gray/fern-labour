from dishka import Provider, Scope, provide

from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.repository import UserRepository


class UserApplicationProvider(Provider):
    component = ComponentEnum.USER
    scope = Scope.REQUEST

    @provide
    def provide_user_service(self, user_repository: UserRepository) -> UserQueryService:
        return UserQueryService(user_repository=user_repository)
