from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.subscription.enums import ContactMethod
from app.notification.domain.entity import Notification
from app.notification.domain.enums import NotificationStatus
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.value_objects.notification_id import NotificationId
from app.notification.infrastructure.persistence.tables.notifications import notifications_table
from app.user.domain.value_objects.user_id import UserId


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

    async def filter(
        self,
        labour_id: LabourId | None = None,
        birthing_person_id: UserId | None = None,
        subscriber_id: UserId | None = None,
        notification_type: ContactMethod | None = None,
        notification_status: NotificationStatus | None = None,
    ) -> list[Notification]:
        """
        Filter notifications based on inputs.

        Args:
            labour_id: An optional Labour ID
            birthing_person_id: An optional Birthing Person ID
            subscriber_id: An optional Subscriber ID
            type: An optional type of notification
            notification_status: An optional notification status

        Returns:
            A list of notifications
        """
        stmt = select(Notification)
        if labour_id:
            stmt = stmt.where(notifications_table.c.labour_id == labour_id.value)
        if subscriber_id:
            stmt = stmt.where(notifications_table.c.subscriber_id == subscriber_id.value)
        if birthing_person_id:
            stmt = stmt.where(notifications_table.c.birthing_person_id == birthing_person_id.value)
        if notification_type:
            stmt = stmt.where(notifications_table.c.type == notification_type.value)
        if notification_status:
            stmt = stmt.where(notifications_table.c.status == notification_status.value)

        result = await self._session.execute(stmt)
        return list(result.scalars())

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
