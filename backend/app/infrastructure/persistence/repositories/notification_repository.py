from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.labour.vo_labour_id import LabourId
from app.domain.notification.entity import Notification
from app.domain.notification.enums import NotificationStatus
from app.domain.notification.repository import NotificationRepository
from app.domain.notification.vo_notification_id import NotificationId
from app.domain.subscription.enums import ContactMethod
from app.domain.user.vo_user_id import UserId
from app.infrastructure.persistence.tables.notifications import notifications_table


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
