import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.infrastructure.persistence.repositories.subscription_repository import (
    SQLAlchemySubscriptionRepository,
)

log = logging.getLogger(__name__)


class SubscriptionInfrastructureProvider(Provider):
    component = ComponentEnum.SUBSCRIPTION
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_subscription_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> SubscriptionRepository:
        return SQLAlchemySubscriptionRepository(session=async_session)
