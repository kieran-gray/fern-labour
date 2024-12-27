import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.labour.repository import LabourRepository
from app.infrastructure.persistence.repositories.birthing_person_repository import (
    SQLAlchemyBirthingPersonRepository,
)
from app.infrastructure.persistence.repositories.labour_repository import SQLAlchemyLabourRepository
from app.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class LabourInfrastructureProvider(Provider):
    component = ComponentEnum.LABOUR
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def provide_labour_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> LabourRepository:
        return SQLAlchemyLabourRepository(session=async_session)

    @provide(scope=Scope.REQUEST)
    def provide_birthing_person_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> BirthingPersonRepository:
        return SQLAlchemyBirthingPersonRepository(session=async_session)
