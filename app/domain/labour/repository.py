from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.labour.entity import Labour


class LabourRepository(ABC):
    """Repository interface for LaborSession aggregate root"""

    @abstractmethod
    async def save(self, labor_session: Labour) -> None:
        """
        Save or update a labor session.

        Args:
            labor_session: The labor session to save
        """

    @abstractmethod
    async def delete(self, labor_session: Labour) -> None:
        """
        Delete a labor session.

        Args:
            labor_session: The labor session to delete
        """

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Labour | None:
        """
        Retrieve a labor session by its ID.

        Args:
            session_id: The ID of the labor session to retrieve

        Returns:
            The labor session if found, None otherwise
        """

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Labour]:
        """
        Retrieve all labor sessions for a given user.

        Args:
            user_id: The ID of the user

        Returns:
            List of labor sessions
        """

    @abstractmethod
    async def get_active_session(self, user_id: UUID) -> Labour | None:
        """
        Retrieve the active labor session for a user, if any exists.
        A user should only have one active session at a time.

        Args:
            user_id: The ID of the user

        Returns:
            The active labor session if found, None otherwise
        """

    @abstractmethod
    async def get_sessions_between(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> list[Labour]:
        """
        Retrieve all labor sessions for a user within a date range.

        Args:
            user_id: The ID of the user
            start_date: Start of the date range
            end_date: End of the date range

        Returns:
            List of labor sessions within the date range
        """
