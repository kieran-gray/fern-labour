import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.labour.domain.labour.repository import LabourRepository
from src.labour.infrastructure.persistence.repositories.labour_repository import (
    SQLAlchemyLabourRepository,
)
from src.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class LabourInfrastructureProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_labour_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> LabourRepository:
        return SQLAlchemyLabourRepository(session=async_session)
