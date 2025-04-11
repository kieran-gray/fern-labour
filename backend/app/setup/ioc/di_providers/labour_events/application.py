from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.domain.producer import EventProducer
from app.labour.application.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.user.application.services.user_query_service import UserQueryService


class LabourEventsApplicationProvider(Provider):
    component = ComponentEnum.LABOUR_EVENTS
    scope = Scope.REQUEST

    @provide
    def get_labour_update_posted_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourUpdatePostedEventHandler:
        return LabourUpdatePostedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            event_producer=event_producer,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_begun_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourBegunEventHandler:
        return LabourBegunEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            event_producer=event_producer,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_completed_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourCompletedEventHandler:
        return LabourCompletedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            event_producer=event_producer,
            tracking_link=settings.notifications.email.tracking_link,
        )
