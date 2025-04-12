from typing import Protocol

from app.notification.domain.entity import Notification
from app.notification.domain.value_objects.notification_id import NotificationId


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
