import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.labour.application.security.token_generator import TokenGenerator
from src.labour.domain.labour.repository import LabourRepository
from src.labour.infrastructure.persistence.repositories.labour_repository import (
    SQLAlchemyLabourRepository,
)
from src.labour.infrastructure.security.sha256_token_generator import SHA256TokenGenerator
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings

log = logging.getLogger(__name__)


class LabourInfrastructureProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_labour_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> LabourRepository:
        return SQLAlchemyLabourRepository(session=async_session)

    @provide
    def provide_token_generator(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> TokenGenerator:
        return SHA256TokenGenerator(settings.security.subscriber_token.salt)
