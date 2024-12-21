from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.labour.entity import Labour


class LabourRepository(ABC):
    """Repository interface for LaborSession aggregate root"""

    @abstractmethod
    async def save(self, labour: Labour) -> None:
        """
        Save or update a labor.

        Args:
            labour: The labor to save
        """

    @abstractmethod
    async def delete(self, labour: Labour) -> None:
        """
        Delete a labor session.

        Args:
            labour: The labor to delete
        """

    @abstractmethod
    async def get_by_id(self, labour_id: UUID) -> Labour | None:
        """
        Retrieve a labor by its ID.

        Args:
            labour_id: The ID of the labor to retrieve

        Returns:
            The labor if found, None otherwise
        """
