from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.core.domain.producer import EventProducer
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_invite_service import LabourInviteService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.user.application.services.user_query_service import UserQueryService


class InvitesApplicationProvider(Provider):
    component = ComponentEnum.INVITES
    scope = Scope.REQUEST

    @provide
    def provide_labour_invite_service(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        subscription_query_service: Annotated[
            SubscriptionQueryService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
        ],
        token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    ) -> LabourInviteService:
        return LabourInviteService(
            user_service=user_service,
            event_producer=event_producer,
            subscription_query_service=subscription_query_service,
            token_generator=token_generator,
        )

    @provide
    def provide_subscriber_invite_service(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriberInviteService:
        return SubscriberInviteService(
            user_service=user_service,
            event_producer=event_producer,
        )
