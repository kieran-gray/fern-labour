# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.domain.repositories.labor_session_repository import LaborSessionRepository
from app.infrastructure.persistence.repositories.labor_session_repository import (
    SQLAlchemyLaborSessionRepository,
)


class LaborSessionRepositoriesProvider(Provider):
    labor_session_repository = provide(
        source=SQLAlchemyLaborSessionRepository,
        scope=Scope.REQUEST,
        provides=LaborSessionRepository,
    )
