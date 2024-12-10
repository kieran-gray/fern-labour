# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.application.services.account_service import AccountService
from app.application.services.authentication_service import AuthenticationService
from app.application.services.authorization_service import AuthorizationService
from app.application.services.token_service import TokenService
from app.application.services.user_service import UserService
from app.application.services.user_session_service import UserSessionService


class UserApplicationProvider(Provider):
    account_service = provide(
        source=AccountService,
        scope=Scope.REQUEST,
    )
    user_service = provide(
        source=UserService,
        scope=Scope.REQUEST,
    )
    authentication_service = provide(
        source=AuthenticationService,
        scope=Scope.REQUEST,
    )
    session_service = provide(
        source=UserSessionService,
        scope=Scope.REQUEST,
    )
    token_service = provide(
        source=TokenService,
        scope=Scope.REQUEST,
    )
    authorization_service = provide(
        source=AuthorizationService,
        scope=Scope.REQUEST,
    )
