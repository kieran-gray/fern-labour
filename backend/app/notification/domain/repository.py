from typing import Protocol

from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.subscription.enums import ContactMethod
from app.notification.domain.entity import Notification
from app.notification.domain.enums import NotificationStatus
from app.notification.domain.value_objects.notification_id import NotificationId
from app.user.domain.value_objects.user_id import UserId


class NotificationRepository(Protocol):
    """Repository interface for Notification entity"""

    async def save(self, notification: Notification) -> None:
        """
        Save or update a Notification.

        Args:
            Notification: The Notification to save
        """

    async def delete(self, notification: Notification) -> None:
        """
        Delete a Notification.

        Args:
            Notification: The Notification to delete
        """

    async def filter(
        self,
        labour_id: LabourId | None = None,
        from_user_id: UserId | None = None,
        to_user_id: UserId | None = None,
        notification_type: ContactMethod | None = None,
        notification_status: NotificationStatus | None = None,
    ) -> list[Notification]:
        """
        Filter Notifications based on inputs.

        Args:
            labour_id: An optional Labour ID
            from_user_id: An optional User ID, representing the sender of the notification
            to_user_id: An optional User ID, representing the receiver of the notification
            notification_type: An optional type of notification
            notification_status: An optional Notification status

        Returns:
            A list of Notifications
        """

    async def get_by_id(self, notification_id: NotificationId) -> Notification | None:
        """
        Retrieve a Notification by ID.

        Args:
            notification_id: The ID of the Notification to retrieve

        Returns:
            The Notification if found, else returns None
        """

    async def get_by_external_id(self, external_id: str) -> Notification | None:
        """
        Retrieve a Notification by external ID.

        Args:
            external_id: The external ID of the Notification to retrieve

        Returns:
            The Notification if found, else returns None
        """

    async def get_by_ids(self, notification_ids: list[NotificationId]) -> list[Notification]:
        """
        Retrieve a list of Notifications by IDs.

        Args:
            Notification_ids: The IDs of the Notifications to retrieve

        Returns:
            A list of Notifications
        """

    async def get_by_external_ids(self, external_ids: list[str]) -> list[Notification]:
        """
        Retrieve a list of Notifications by external IDs.

        Args:
            external_ids: The external IDs of the Notifications to retrieve

        Returns:
            A list of Notifications
        """
