from dishka import Provider, Scope, provide

from app.domain.birthing_person.repository import BirthingPersonRepository
from app.infrastructure.persistence.repositories.birthing_person_repository import (
    SQLAlchemyBirthingPersonRepository,
)


class BirthingPersonRepositoriesProvider(Provider):
    birthing_person_repository = provide(
        source=SQLAlchemyBirthingPersonRepository,
        scope=Scope.REQUEST,
        provides=BirthingPersonRepository,
    )
