from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_invite_service import LabourInviteService
from app.notification.application.services.email_generation_service import EmailGenerationService
from app.notification.application.services.notification_service import NotificationService
from app.setup.ioc.di_component_enum import ComponentEnum
from app.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.user.application.services.user_service import UserService


class InvitesApplicationProvider(Provider):
    component = ComponentEnum.INVITES
    scope = Scope.REQUEST

    @provide
    def provide_labour_invite_service(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
        token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    ) -> LabourInviteService:
        return LabourInviteService(
            user_service=user_service,
            notification_service=notification_service,
            subscription_query_service=subscription_query_service,
            email_generation_service=email_generation_service,
            token_generator=token_generator,
        )

    @provide
    def provide_subscriber_invite_service(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
    ) -> SubscriberInviteService:
        return SubscriberInviteService(
            user_service=user_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
        )
