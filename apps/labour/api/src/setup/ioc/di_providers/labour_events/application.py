from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.core.application.notification_service_client import NotificationServiceClient
from src.labour.application.event_handlers.labour_begun_event_handler import (
    LabourBegunEventHandler,
)
from src.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from src.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.user.application.services.user_query_service import UserQueryService


class LabourEventsApplicationProvider(Provider):
    component = ComponentEnum.LABOUR_EVENTS
    scope = Scope.REQUEST

    @provide
    def get_labour_update_posted_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTION)
        ],
        notification_service_client: Annotated[
            NotificationServiceClient, FromComponent(ComponentEnum.DEFAULT)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourUpdatePostedEventHandler:
        return LabourUpdatePostedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service_client=notification_service_client,
            tracking_link=settings.security.cors.frontend_host,
        )

    @provide
    def get_labour_begun_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTION)
        ],
        notification_service_client: Annotated[
            NotificationServiceClient, FromComponent(ComponentEnum.DEFAULT)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourBegunEventHandler:
        return LabourBegunEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service_client=notification_service_client,
            tracking_link=settings.security.cors.frontend_host,
        )

    @provide
    def get_labour_completed_event_handler(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTION)
        ],
        notification_service_client: Annotated[
            NotificationServiceClient, FromComponent(ComponentEnum.DEFAULT)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourCompletedEventHandler:
        return LabourCompletedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service_client=notification_service_client,
            tracking_link=settings.security.cors.frontend_host,
        )
