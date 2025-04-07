from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.labour.application.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)
from app.notification.application.services.notification_service import NotificationService
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.user.application.services.user_service import UserService


class LabourEventsApplicationProvider(Provider):
    component = ComponentEnum.LABOUR_EVENTS
    scope = Scope.REQUEST

    @provide
    def get_labour_update_posted_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_template_engine: Annotated[
            EmailTemplateEngine, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourUpdatePostedEventHandler:
        return LabourUpdatePostedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service=notification_service,
            email_template_engine=email_template_engine,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_begun_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_template_engine: Annotated[
            EmailTemplateEngine, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourBegunEventHandler:
        return LabourBegunEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service=notification_service,
            email_template_engine=email_template_engine,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_completed_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_template_engine: Annotated[
            EmailTemplateEngine, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourCompletedEventHandler:
        return LabourCompletedEventHandler(
            user_service=user_service,
            subscription_query_service=subscription_query_service,
            notification_service=notification_service,
            email_template_engine=email_template_engine,
            tracking_link=settings.notifications.email.tracking_link,
        )
