from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer

from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
from src.subscription.application.event_handlers.subscriber_approved_event_handler import (
    SubscriberApprovedEventHandler,
)
from src.subscription.application.event_handlers.subscriber_requested_event_handler import (
    SubscriberRequestedEventHandler,
)
from src.user.application.services.user_query_service import UserQueryService


class SubscriptionEventsApplicationProvider(Provider):
    component = ComponentEnum.SUBSCRIPTION_EVENTS
    scope = Scope.REQUEST

    @provide
    def get_subscriber_approved_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> SubscriberApprovedEventHandler:
        return SubscriberApprovedEventHandler(
            user_service=user_service,
            event_producer=event_producer,
            tracking_link=settings.security.cors.frontend_host,
        )

    @provide
    def get_subscriber_requested_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> SubscriberRequestedEventHandler:
        return SubscriberRequestedEventHandler(
            user_service=user_service,
            event_producer=event_producer,
            tracking_link=settings.security.cors.frontend_host,
        )
