from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.domain.producer import EventProducer
from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_invite_service import LabourInviteService
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
        user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> SubscriberInviteService:
        return SubscriberInviteService(
            user_service=user_service,
            event_producer=event_producer,
        )
