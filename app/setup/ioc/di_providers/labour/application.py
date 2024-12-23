from dishka import Provider, Scope, provide

from app.application.services.labour_service import LabourService
from app.application.services.get_labour_service import GetLabourService


class LabourApplicationProvider(Provider):
    labour_service = provide(
        source=LabourService,
        scope=Scope.REQUEST,
    )

    get_labour_service = provide(
        source=GetLabourService,
        scope=Scope.REQUEST
    )
