from dishka import Provider, Scope, provide

from app.domain.labour.repository import LabourRepository
from app.infrastructure.persistence.repositories.labour_repository import SQLAlchemyLabourRepository


class LabourRepositoriesProvider(Provider):
    labour_repository = provide(
        source=SQLAlchemyLabourRepository,
        scope=Scope.REQUEST,
        provides=LabourRepository,
    )
