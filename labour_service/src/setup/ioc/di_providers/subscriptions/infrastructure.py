import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.labour.application.security.token_generator import TokenGenerator
from src.labour.infrastructure.security.sha256_token_generator import SHA256TokenGenerator
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.infrastructure.persistence.repositories.subscription_repository import (
    SQLAlchemySubscriptionRepository,
)

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
