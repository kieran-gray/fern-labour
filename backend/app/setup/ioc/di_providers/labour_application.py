from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.producer import EventProducer
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_invite_service import LabourInviteService
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_service import SubscriptionService
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.labour.repository import LabourRepository
from app.setup.ioc.di_component_enum import ComponentEnum


class LabourApplicationProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.REQUEST

    @provide
    def provide_birthing_person_service(
        self,
        birthing_person_repository: BirthingPersonRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> BirthingPersonService:
        return BirthingPersonService(
            birthing_person_repository=birthing_person_repository, event_producer=event_producer
        )

    @provide
    def provide_labour_service(
        self,
        birthing_person_service: BirthingPersonService,
        labour_repository: LabourRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> LabourService:
        return LabourService(
            birthing_person_service=birthing_person_service,
            labour_repository=labour_repository,
            event_producer=event_producer,
        )

    @provide
    def provide_labour_invite_service(
        self,
        birthing_person_service: BirthingPersonService,
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
        subscription_service: Annotated[
            SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)
        ],
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.SUBSCRIBER)],
    ) -> LabourInviteService:
        return LabourInviteService(
            birthing_person_service=birthing_person_service,
            notification_service=notification_service,
            subscriber_service=subscriber_service,
            subscription_service=subscription_service,
            email_generation_service=email_generation_service,
            token_generator=token_generator,
        )

    @provide
    def provide_get_labour_service(self, labour_repository: LabourRepository) -> GetLabourService:
        return GetLabourService(labour_repository=labour_repository)
