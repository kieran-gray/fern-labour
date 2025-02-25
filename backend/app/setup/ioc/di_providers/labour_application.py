from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_invite_service import LabourInviteService
from app.application.services.labour_service import LabourService
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.domain.labour.repository import LabourRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class LabourApplicationProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.REQUEST

    @provide
    def provide_labour_service(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        labour_repository: LabourRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> LabourService:
        return LabourService(
            user_service=user_service,
            labour_repository=labour_repository,
            event_producer=event_producer,
        )

    @provide
    def provide_labour_invite_service(
        self,
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        subscription_service: Annotated[
            SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    ) -> LabourInviteService:
        return LabourInviteService(
            user_service=user_service,
            notification_service=notification_service,
            subscription_service=subscription_service,
            email_generation_service=email_generation_service,
            token_generator=token_generator,
        )

    @provide
    def provide_get_labour_service(self, labour_repository: LabourRepository) -> GetLabourService:
        return GetLabourService(labour_repository=labour_repository)
