from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_query_service import LabourQueryService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.repository import SubscriptionRepository


class SubscriptionApplicationProvider(Provider):
    component = ComponentEnum.SUBSCRIPTION
    scope = Scope.REQUEST

    @provide
    def provide_subscription_authorization_service(
        self,
        subscription_repository: SubscriptionRepository,
    ) -> SubscriptionAuthorizationService:
        return SubscriptionAuthorizationService(subscription_repository=subscription_repository)

    @provide
    def provide_subscription_service(
        self,
        subscription_repository: SubscriptionRepository,
        domain_event_repository: Annotated[
            DomainEventRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        unit_of_work: Annotated[UnitOfWork, FromComponent(ComponentEnum.DEFAULT)],
        labour_query_service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
        token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.LABOUR)],
        domain_event_publisher: Annotated[
            DomainEventPublisher, FromComponent(ComponentEnum.DEFAULT)
        ],
    ) -> SubscriptionService:
        return SubscriptionService(
            subscription_repository=subscription_repository,
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            labour_query_service=labour_query_service,
            token_generator=token_generator,
            domain_event_publisher=domain_event_publisher,
        )

    @provide
    def provide_subscription_query_service(
        self,
        subscription_repository: SubscriptionRepository,
        subscription_authorization_service: SubscriptionAuthorizationService,
    ) -> SubscriptionQueryService:
        return SubscriptionQueryService(
            subscription_repository=subscription_repository,
            subscription_authorization_service=subscription_authorization_service,
        )

    @provide
    def provide_subscription_management_service(
        self,
        subscription_repository: SubscriptionRepository,
        domain_event_repository: Annotated[
            DomainEventRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        unit_of_work: Annotated[UnitOfWork, FromComponent(ComponentEnum.DEFAULT)],
        subscription_authorization_service: SubscriptionAuthorizationService,
        domain_event_publisher: Annotated[
            DomainEventPublisher, FromComponent(ComponentEnum.DEFAULT)
        ],
    ) -> SubscriptionManagementService:
        return SubscriptionManagementService(
            subscription_repository=subscription_repository,
            domain_event_repository=domain_event_repository,
            unit_of_work=unit_of_work,
            subscription_authorization_service=subscription_authorization_service,
            domain_event_publisher=domain_event_publisher,
        )
