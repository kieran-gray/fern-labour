from typing import Any

from app.domain.base.exceptions import DomainError


class BirthingPersonNotFoundById(DomainError):
    def __init__(self, birthing_person_id: Any) -> None:
        super().__init__(f"Birthing Person with id '{birthing_person_id}' is not found.")


class BirthingPersonExistsWithID(DomainError):
    def __init__(self, birthing_person_id: Any) -> None:
        super().__init__(f"Birthing Person with id '{birthing_person_id}' already exists.")


class BirthingPersonHasActiveLabour(DomainError):
    def __init__(self, birthing_person_id: Any) -> None:
        super().__init__(f"Birthing Person '{birthing_person_id}' already has an active labour")


class BirthingPersonDoesNotHaveActiveLabour(DomainError):
    def __init__(self, birthing_person_id: Any) -> None:
        super().__init__(f"Birthing Person '{birthing_person_id}' does not have an active labour")
