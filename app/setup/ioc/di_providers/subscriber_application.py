from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_service import SubscriptionService
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.subscriber.repository import SubscriberRepository
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
        birthing_person_repository: Annotated[
            BirthingPersonRepository, FromComponent(ComponentEnum.LABOUR)
        ],
        subscriber_repository: SubscriberRepository,
        token_generator: TokenGenerator,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriptionService:
        return SubscriptionService(
            birthing_person_repository=birthing_person_repository,
            subscriber_repository=subscriber_repository,
            token_generator=token_generator,
            event_producer=event_producer,
        )
