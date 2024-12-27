import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.security.token_generator import TokenGenerator
from app.domain.subscriber.repository import SubscriberRepository
from app.infrastructure.persistence.repositories.subscriber_repository import (
    SQLAlchemySubscriberRepository,
)
from app.infrastructure.security.sha256_token_generator import SHA256TokenGenerator
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class SubscriberInfrastructureProvider(Provider):
    component = ComponentEnum.SUBSCRIBER
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_subscriber_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> SubscriberRepository:
        return SQLAlchemySubscriberRepository(session=async_session)

    @provide
    def provide_token_generator(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> TokenGenerator:
        return SHA256TokenGenerator(settings.security.subscriber_token.salt)
