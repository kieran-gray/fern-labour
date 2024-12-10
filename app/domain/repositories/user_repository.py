from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    """Repository interface for User entity"""

    @abstractmethod
    async def save(self, user: User) -> None:
        """
        Save or update a user.

        Args:
            user: The user to save
        """

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """
        Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete
        """

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email: The email address to look up

        Returns:
            The user if found, None otherwise
        """

    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """
        Check if a user exists with the given email.

        Args:
            email: The email address to check

        Returns:
            True if a user exists with this email, False otherwise
        """

    # @abstractmethod
    # async def get_session(self, user_id: UUID) -> UserSession | None:
    #     """
    #     Get session for user with given user_id if exists.

    #     Args:
    #         user_id: The ID of the user to retrieve session for

    #     Returns:
    #         The user session if found, None otherwise
    #     """
