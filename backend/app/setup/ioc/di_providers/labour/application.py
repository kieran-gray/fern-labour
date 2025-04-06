from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.infrastructure.events.interfaces.producer import EventProducer
from app.labour.application.security.labour_authorization_service import LabourAuthorizationService
from app.labour.application.services.labour_query_service import LabourQueryService
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.repository import LabourRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class LabourApplicationProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.REQUEST

    @provide
    def provide_labour_service(
        self,
        labour_repository: LabourRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> LabourService:
        return LabourService(
            labour_repository=labour_repository,
            event_producer=event_producer,
        )

    @provide
    def provide_labour_query_service(
        self, labour_repository: LabourRepository
    ) -> LabourQueryService:
        return LabourQueryService(labour_repository=labour_repository)

    @provide
    def provide_labour_authorization_service(self) -> LabourAuthorizationService:
        return LabourAuthorizationService()
