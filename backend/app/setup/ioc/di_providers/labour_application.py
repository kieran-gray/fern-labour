from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.labour.repository import LabourRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class LabourApplicationProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.REQUEST

    @provide
    def provide_labour_service(
        self,
        birthing_person_repository: BirthingPersonRepository,
        labour_repository: LabourRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> LabourService:
        return LabourService(
            birthing_person_repository=birthing_person_repository,
            labour_repository=labour_repository,
            event_producer=event_producer,
        )

    @provide
    def provide_birthing_person_service(
        self,
        birthing_person_repository: BirthingPersonRepository,
    ) -> BirthingPersonService:
        return BirthingPersonService(birthing_person_repository=birthing_person_repository)

    @provide
    def provide_get_labour_service(
        self,
        birthing_person_repository: BirthingPersonRepository,
    ) -> GetLabourService:
        return GetLabourService(birthing_person_repository=birthing_person_repository)
