from typing import Protocol

from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage


class ContactMessageRepository(Protocol):
    """Repository interface for ContactMessage entity"""

    async def save(self, contact_message: ContactMessage) -> None:
        """
        Save or update a contact message.

        Args:
            contact_message: The contact message to save
        """

    async def delete(self, contact_message: ContactMessage) -> None:
        """
        Delete a contact message.

        Args:
            contact_message: The contact message to delete
        """

    async def get_by_id(self, contact_message_id: ContactMessageId) -> ContactMessage | None:
        """
        Retrieve a contact message by ID.

        Args:
            contact message_id: The ID of the contact message to retrieve

        Returns:
            The contact message if found, else returns None
        """

    async def get_by_ids(self, contact_message_ids: list[ContactMessageId]) -> list[ContactMessage]:
        """
        Retrieve a list of contact messages by their IDs.

        Args:
            contact message_ids: The IDs of the contact messages to retrieve

        Returns:
            A list of contact messages
        """
