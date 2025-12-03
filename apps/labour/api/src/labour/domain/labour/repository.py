from typing import Protocol

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.user.domain.value_objects.user_id import UserId


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

    async def get_labours_by_birthing_person_id(self, birthing_person_id: UserId) -> list[Labour]:
        """
        Retrieve an labours by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve labours for

        Returns:
            List of labours
        """

    async def get_active_labour_by_birthing_person_id(
        self, birthing_person_id: UserId
    ) -> Labour | None:
        """
        Retrieve an active labour by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve the labour for

        Returns:
            The labour if found, None otherwise
        """

    async def get_active_labour_id_by_birthing_person_id(
        self, birthing_person_id: UserId
    ) -> LabourId | None:
        """
        Retrieve an ID for the active labour by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve the labour ID for

        Returns:
            The labour ID if found, None otherwise
        """

    async def get_birthing_person_id_for_labour(self, labour_id: LabourId) -> UserId | None:
        """
        Retrieve a the birthing person who owns the labour associated with the provided labour id

        Args:
            labour_id: The ID of the labour

        Returns:
            The UserId of the birthing person if found, None otherwise
        """
