from dishka import Provider, Scope, provide

from app.application.services.begin_labour_service import UserService


class UserApplicationProvider(Provider):
    user_service = provide(
        source=UserService,
        scope=Scope.REQUEST,
    )
