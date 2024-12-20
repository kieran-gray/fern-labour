from typing import Any

from app.domain.base.exceptions import DomainError
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId


class BirthingPersonNotFoundById(DomainError):
    def __init__(self, birthing_person_id: Any):
        super().__init__(f"Birthing Person with id '{birthing_person_id}' is not found.")


class c(DomainError):
    def __init__(self, birthing_person_id: Any):
        super().__init__(f"Birthing Person with id '{birthing_person_id}' already exists.")


class ContactAlreadyExists(DomainError):
    def __init__(self):
        super().__init__("Contact already exists on birthing person")


class ContactDoesNotExist(DomainError):
    def __init__(self):
        super().__init__("Contact does not exist on birthing person")


class BirthingPersonHasActiveLabour(DomainError):
    def __init__(self, id: BirthingPersonId):
        super().__init__(f"Birthing Person '{id}' already has an active labour")


class BirthingPersonDoesNotHaveActiveLabour(DomainError):
    def __init__(self, id: BirthingPersonId):
        super().__init__(f"Birthing Person '{id}' does not have an active labour")


class LabourAlreadyExists(DomainError):
    def __init__(self):
        super().__init__("Labour already exists on birthing person")
