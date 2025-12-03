from typing import Protocol

from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId


class UserRepository(Protocol):
    """Repository interface for User entity"""

    async def save(self, user: User) -> None:
        """
        Save or update a user.

        Args:
            user: The user to save
        """

    async def delete(self, user: User) -> None:
        """
        Delete a user.

        Args:
            user: The user to delete
        """

    async def get_by_id(self, user_id: UserId) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The user if found, else returns None
        """

    async def get_by_ids(self, user_ids: list[UserId]) -> list[User]:
        """
        Retrieve a list of users by their IDs.

        Args:
            user_ids: The IDs of the users to retrieve

        Returns:
            A list of users
        """
