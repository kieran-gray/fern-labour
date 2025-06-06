from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.application.unit_of_work import UnitOfWork
from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.security.labour_authorization_service import LabourAuthorizationService
from src.labour.application.services.contraction_service import ContractionService
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.repository import LabourRepository
from src.setup.ioc.di_component_enum import ComponentEnum


class LabourApplicationProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.REQUEST

    @provide
    def provide_labour_service(
        self,
        labour_repository: LabourRepository,
        domain_event_repository: Annotated[
            DomainEventRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        unit_of_work: Annotated[UnitOfWork, FromComponent(ComponentEnum.DEFAULT)],
        domain_event_publisher: Annotated[
            DomainEventPublisher, FromComponent(ComponentEnum.DEFAULT)
        ],
    ) -> LabourService:
        return LabourService(
            labour_repository=labour_repository,
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            domain_event_publisher=domain_event_publisher,
        )

    @provide
    def provide_contraction_service(
        self,
        labour_repository: LabourRepository,
        domain_event_repository: Annotated[
            DomainEventRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        unit_of_work: Annotated[UnitOfWork, FromComponent(ComponentEnum.DEFAULT)],
        domain_event_publisher: Annotated[
            DomainEventPublisher, FromComponent(ComponentEnum.DEFAULT)
        ],
    ) -> ContractionService:
        return ContractionService(
            labour_repository=labour_repository,
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            domain_event_publisher=domain_event_publisher,
        )

    @provide
    def provide_labour_query_service(
        self, labour_repository: LabourRepository
    ) -> LabourQueryService:
        return LabourQueryService(labour_repository=labour_repository)

    @provide
    def provide_labour_authorization_service(
        self, labour_repository: LabourRepository
    ) -> LabourAuthorizationService:
        return LabourAuthorizationService(labour_repository=labour_repository)
