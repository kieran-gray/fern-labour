from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.notification.application.event_handlers.notification_requested_event_handler import (
    NotificationRequestedEventHandler,
)
from src.notification.application.services.notification_service import NotificationService
from src.setup.ioc.di_component_enum import ComponentEnum


class NotificationEventsApplicationProvider(Provider):
    component = ComponentEnum.NOTIFICATION_EVENTS
    scope = Scope.REQUEST

    @provide
    def get_notification_requested_event_handler(
        self,
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
    ) -> NotificationRequestedEventHandler:
        return NotificationRequestedEventHandler(notification_service=notification_service)
