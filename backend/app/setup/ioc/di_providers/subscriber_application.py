from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscription.repository import SubscriptionRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class SubscriberApplicationProvider(Provider):
    component = ComponentEnum.SUBSCRIBER
    scope = Scope.REQUEST

    @provide
    def provide_subscriber_service(
        self,
        subscriber_repository: SubscriberRepository,
        token_generator: TokenGenerator,
    ) -> SubscriberService:
        return SubscriberService(
            subscriber_repository=subscriber_repository,
            token_generator=token_generator,
        )

    @provide
    def provide_subscription_service(
        self,
        subscription_repository: Annotated[
            SubscriptionRepository, FromComponent(ComponentEnum.SUBSCRIBER)
        ],
        subscriber_service: SubscriberService,
        get_labour_service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
        token_generator: TokenGenerator,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriptionService:
        return SubscriptionService(
            subscription_repository=subscription_repository,
            subscriber_service=subscriber_service,
            get_labour_service=get_labour_service,
            token_generator=token_generator,
            event_producer=event_producer,
        )

    @provide
    def provide_subscription_management_service(
        self,
        subscription_repository: Annotated[
            SubscriptionRepository, FromComponent(ComponentEnum.SUBSCRIBER)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriptionManagementService:
        return SubscriptionManagementService(
            subscription_repository=subscription_repository,
            event_producer=event_producer,
        )
