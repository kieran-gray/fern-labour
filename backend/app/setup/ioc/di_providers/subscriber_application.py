from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.notification.application.services.email_generation_service import EmailGenerationService
from app.notification.application.services.notification_service import NotificationService
from app.setup.ioc.di_component_enum import ComponentEnum
from app.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from app.user.application.services.user_service import UserService


class SubscriberApplicationProvider(Provider):
    component = ComponentEnum.SUBSCRIBER
    scope = Scope.REQUEST

    @provide
    def provide_subscriber_invite_service(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
    ) -> SubscriberInviteService:
        return SubscriberInviteService(
            user_service=user_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
        )
