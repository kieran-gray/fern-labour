from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.infrastructure.persistence.tables.subscribers import subscribers_table


class SQLAlchemySubscriberRepository(SubscriberRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, subscriber: Subscriber) -> None:
        """
        Save or update a subscriber.

        Args:
            subscriber: The subscriber to save
        """
        self._session.add(subscriber)
        await self._session.commit()

    async def delete(self, subscriber: Subscriber) -> None:
        """
        Delete a subscriber.

        Args:
            subscriber: The subscriber to delete
        """

        await self._session.delete(subscriber)
        await self._session.commit()

    async def get_by_id(self, subscriber_id: SubscriberId) -> Subscriber | None:
        """
        Retrieve a subscriber by their ID.

        Args:
            subscriber_id: The ID of the subscriber to retrieve

        Returns:
            The subscriber if found, None otherwise
        """
        stmt = select(Subscriber).where(subscribers_table.c.id == subscriber_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
