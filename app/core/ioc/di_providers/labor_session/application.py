# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.application.services.labor_session_service import LaborSessionService


class LaborSessionApplicationProvider(Provider):
    labor_session_service = provide(
        source=LaborSessionService,
        scope=Scope.REQUEST,
    )
