from typing import Protocol

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId


class LabourRepository(Protocol):
    """Repository interface for Labour aggregate root"""

    async def save(self, labour: Labour) -> None:
        """
        Save or update a labour.

        Args:
            labour: The labour to save
        """

    async def delete(self, labour: Labour) -> None:
        """
        Delete a labour.

        Args:
            labour: The labour to delete
        """

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        """
        Retrieve a labour by its ID.

        Args:
            labour_id: The ID of the labour to retrieve

        Returns:
            The labour if found, None otherwise
        """

    async def get_labours_by_birthing_person_id(
        self, birthing_person_id: BirthingPersonId
    ) -> list[Labour]:
        """
        Retrieve an labours by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve labours for

        Returns:
            List of labours
        """

    async def get_active_labour_by_birthing_person_id(
        self, birthing_person_id: BirthingPersonId
    ) -> Labour | None:
        """
        Retrieve an active labour by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve the labour for

        Returns:
            The labour if found, None otherwise
        """
