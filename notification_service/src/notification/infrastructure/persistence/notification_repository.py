from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationStatus
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId
from src.notification.infrastructure.persistence.tables import notifications_table


class SQLAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

        """Repository interface for Notification entity"""

    async def save(self, notification: Notification) -> None:
        """
        Save or update a notification.

        Args:
            notification: The notification to save
        """
        self._session.add(notification)
        await self._session.commit()

    async def delete(self, notification: Notification) -> None:
        """
        Delete a notification.

        Args:
            notification: The notification to delete
        """
        await self._session.delete(notification)
        await self._session.commit()

    async def get_by_id(self, notification_id: NotificationId) -> Notification | None:
        """
        Retrieve a notification by ID.

        Args:
            notification_id: The ID of the notification to retrieve

        Returns:
            The notification if found, else returns None
        """
        stmt = select(Notification).where(notifications_table.c.id == notification_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_external_id(self, external_id: str) -> Notification | None:
        """
        Retrieve a Notification by external ID.

        Args:
            external_id: The external ID of the Notification to retrieve

        Returns:
            The Notification if found, else returns None
        """
        stmt = select(Notification).where(notifications_table.c.external_id == external_id)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids(self, notification_ids: list[NotificationId]) -> list[Notification]:
        """
        Retrieve a list of notifications by IDs.

        Args:
            notification_ids: The IDs of the notifications to retrieve

        Returns:
            A list of notifications
        """
        stmt = select(Notification).where(
            notifications_table.c.id.in_([s.value for s in notification_ids])
        )

        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def get_by_external_ids(self, external_ids: list[str]) -> list[Notification]:
        """
        Retrieve a list of Notifications by external IDs.

        Args:
            external_ids: The external IDs of the Notifications to retrieve

        Returns:
            A list of Notifications
        """
        stmt = select(Notification).where(notifications_table.c.external_id.in_(external_ids))

        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def get_undelivered_notifications(self) -> list[Notification]:
        """
        Retrieve all undelivered notifications.

        An undelivered notification has an external_id and status of 'sent'.

        Returns:
            A list of undelivered notifications
        """
        stmt = select(Notification).where(
            and_(
                notifications_table.c.external_id.is_not(None),
                notifications_table.c.status == NotificationStatus.SENT,
            )
        )
        result = await self._session.execute(stmt)
        return list(result.scalars())
