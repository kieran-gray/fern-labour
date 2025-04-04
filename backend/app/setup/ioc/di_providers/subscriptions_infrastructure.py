import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.labour.application.security.token_generator import TokenGenerator
from app.labour.domain.subscription.repository import SubscriptionRepository
from app.labour.infrastructure.persistence.repositories.subscription_repository import (
    SQLAlchemySubscriptionRepository,
)
from app.labour.infrastructure.security.sha256_token_generator import SHA256TokenGenerator
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class SubscriptionsInfrastructureProvider(Provider):
    component = ComponentEnum.SUBSCRIPTIONS
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_subscription_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> SubscriptionRepository:
        return SQLAlchemySubscriptionRepository(session=async_session)

    @provide
    def provide_token_generator(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> TokenGenerator:
        return SHA256TokenGenerator(settings.security.subscriber_token.salt)
