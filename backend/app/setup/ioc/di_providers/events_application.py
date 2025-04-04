from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.labour.application.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings


class EventsApplicationProvider(Provider):
    component = ComponentEnum.EVENTS
    scope = Scope.REQUEST

    @provide
    def get_labour_update_posted_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_service: Annotated[
            SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourUpdatePostedEventHandler:
        return LabourUpdatePostedEventHandler(
            user_service=user_service,
            subscription_service=subscription_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_begun_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_service: Annotated[
            SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourBegunEventHandler:
        return LabourBegunEventHandler(
            user_service=user_service,
            subscription_service=subscription_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
            tracking_link=settings.notifications.email.tracking_link,
        )

    @provide
    def get_labour_completed_event_handler(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        subscription_service: Annotated[
            SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourCompletedEventHandler:
        return LabourCompletedEventHandler(
            user_service=user_service,
            subscription_service=subscription_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
            tracking_link=settings.notifications.email.tracking_link,
        )
