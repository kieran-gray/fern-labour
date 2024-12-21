from dishka import Provider, Scope, provide

from app.application.services.labour_service import LabourService


class LabourApplicationProvider(Provider):
    labour_service = provide(
        source=LabourService,
        scope=Scope.REQUEST,
    )
