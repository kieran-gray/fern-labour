from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.domain.producer import EventProducer
from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_query_service import LabourQueryService
from app.setup.ioc.di_component_enum import ComponentEnum
from app.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from app.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.application.services.subscription_service import SubscriptionService
from app.subscription.domain.repository import SubscriptionRepository


class SubscriptionsApplicationProvider(Provider):
    component = ComponentEnum.SUBSCRIPTIONS
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
        labour_query_service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
        token_generator: TokenGenerator,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriptionService:
        return SubscriptionService(
            subscription_repository=subscription_repository,
            labour_query_service=labour_query_service,
            token_generator=token_generator,
            event_producer=event_producer,
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
        subscription_authorization_service: SubscriptionAuthorizationService,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriptionManagementService:
        return SubscriptionManagementService(
            subscription_repository=subscription_repository,
            subscription_authorization_service=subscription_authorization_service,
            event_producer=event_producer,
        )
