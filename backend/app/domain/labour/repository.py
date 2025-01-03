from typing import Protocol

from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId


class LabourRepository(Protocol):
    """Repository interface for LaborSession aggregate root"""

    async def save(self, labour: Labour) -> None:
        """
        Save or update a labor.

        Args:
            labour: The labor to save
        """

    async def delete(self, labour: Labour) -> None:
        """
        Delete a labor session.

        Args:
            labour: The labor to delete
        """

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        """
        Retrieve a labor by its ID.

        Args:
            labour_id: The ID of the labor to retrieve

        Returns:
            The labor if found, None otherwise
        """
