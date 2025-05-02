from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.core.domain.producer import EventProducer
from src.core.infrastructure.security.rate_limiting.interface import RateLimiter
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_invite_service import LabourInviteService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
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
        rate_limiter: Annotated[RateLimiter, FromComponent(ComponentEnum.DEFAULT)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> LabourInviteService:
        return LabourInviteService(
            user_service=user_service,
            event_producer=event_producer,
            subscription_query_service=subscription_query_service,
            token_generator=token_generator,
            rate_limiter=rate_limiter,
            rate_limit=settings.security.rate_limits.labour_invite_limit,
            rate_limit_expiry=settings.security.rate_limits.labour_invite_expiry,
        )

    @provide
    def provide_subscriber_invite_service(
        self,
        user_service: Annotated[UserQueryService, FromComponent(ComponentEnum.USER)],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        rate_limiter: Annotated[RateLimiter, FromComponent(ComponentEnum.DEFAULT)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> SubscriberInviteService:
        return SubscriberInviteService(
            user_service=user_service,
            event_producer=event_producer,
            rate_limiter=rate_limiter,
            rate_limit=settings.security.rate_limits.subscriber_invite_limit,
            rate_limit_expiry=settings.security.rate_limits.subscriber_invite_expiry,
        )
