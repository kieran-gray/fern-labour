# pylint: disable=C0301 (line-too-long)

from dishka import Provider, Scope, provide

from app.domain.labour.repository import LabourRepository
from app.infrastructure.persistence.repositories.labor_session_repository import (
    SQLAlchemyLaborSessionRepository,
)


class LaborSessionRepositoriesProvider(Provider):
    labor_session_repository = provide(
        source=SQLAlchemyLaborSessionRepository,
        scope=Scope.REQUEST,
        provides=LabourRepository,
    )
