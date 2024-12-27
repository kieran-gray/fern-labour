from abc import ABC, abstractmethod

from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.vo_subscriber_id import SubscriberId


class SubscriberRepository(ABC):
    """Repository interface for Subscriber entity"""

    @abstractmethod
    async def save(self, subscriber: Subscriber) -> None:
        """
        Save or update a subscriber.

        Args:
            subscriber: The subscriber to save
        """

    @abstractmethod
    async def delete(self, subscriber: Subscriber) -> None:
        """
        Delete a subscriber.

        Args:
            subscriber: The subscriber to delete
        """

    @abstractmethod
    async def get_by_id(self, subscriber_id: SubscriberId) -> Subscriber | None:
        """
        Retrieve a subscriber by their ID.

        Args:
            subscriber_id: The ID of the subscriber to retrieve

        Returns:
            The subscriber if found, else returns None
        """
