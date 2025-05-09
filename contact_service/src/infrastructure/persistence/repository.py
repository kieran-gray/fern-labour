from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage
from src.domain.repository import ContactMessageRepository
from src.infrastructure.persistence.table import contact_messages_table


class SQLAlchemyContactMessageRepository(ContactMessageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, contact_message: ContactMessage) -> None:
        """
        Save or update a contact_message.

        Args:
            contact_message: The contact_message to save
        """
        self._session.add(contact_message)
        await self._session.commit()

    async def delete(self, contact_message: ContactMessage) -> None:
        """
        Delete a contact_message.

        Args:
            contact_message: The contact message to delete
        """
        await self._session.delete(contact_message)
        await self._session.commit()

    async def get_by_id(self, contact_message_id: ContactMessageId) -> ContactMessage | None:
        """
        Retrieve a contact_message by its ID.

        Args:
            contact_message_id: The ID of the contact message to retrieve

        Returns:
            The contact_message if found, None otherwise
        """
        stmt = select(ContactMessage).where(contact_messages_table.c.id == contact_message_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids(self, contact_message_ids: list[ContactMessageId]) -> list[ContactMessage]:
        """
        Retrieve a list of Contact Messages by IDs.

        Args:
            contact_message_ids: The IDs of the contact messages to retrieve

        Returns:
            A list of contact messages
        """
        stmt = select(ContactMessage).where(
            contact_messages_table.c.id.in_([s.value for s in contact_message_ids])
        )

        result = await self._session.execute(stmt)
        return list(result.scalars())
