from typing import Protocol

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId


class BirthingPersonRepository(Protocol):
    """Repository interface for Birthing Person entity"""

    async def save(self, birthing_person: BirthingPerson) -> None:
        """
        Save or update a birthing_person.

        Args:
            birthing_person: The birthing_person to save
        """

    async def delete(self, birthing_person: BirthingPerson) -> None:
        """
        Delete a birthing_person.

        Args:
            birthing_person: The birthing_person to delete
        """

    async def get_by_id(self, birthing_person_id: BirthingPersonId) -> BirthingPerson | None:
        """
        Retrieve a birthing_person by their ID.

        Args:
            birthing_person_id: The ID of the birthing_person to retrieve

        Returns:
            The birthing_person if found, else returns None
        """
