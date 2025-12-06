from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.core.application.notification_service_client import NotificationServiceClient
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
        notification_service_client: Annotated[
            NotificationServiceClient, FromComponent(ComponentEnum.DEFAULT)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> SubscriberApprovedEventHandler:
        return SubscriberApprovedEventHandler(
            user_service=user_service,
            notification_service_client=notification_service_client,
            tracking_link=settings.security.cors.frontend_host,
        )

    @provide
    def get_subscriber_requested_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        notification_service_client: Annotated[
            NotificationServiceClient, FromComponent(ComponentEnum.DEFAULT)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> SubscriberRequestedEventHandler:
        return SubscriberRequestedEventHandler(
            user_service=user_service,
            notification_service_client=notification_service_client,
            tracking_link=settings.security.cors.frontend_host,
        )
