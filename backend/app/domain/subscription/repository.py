from typing import Protocol

from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.vo_subscription_id import SubscriptionId
from app.domain.user.vo_user_id import UserId


class SubscriptionRepository(Protocol):
    """Repository interface for Subscription entity"""

    async def save(self, subscription: Subscription) -> None:
        """
        Save or update a subscription.

        Args:
            subscription: The subscription to save
        """

    async def delete(self, subscription: Subscription) -> None:
        """
        Delete a subscription.

        Args:
            subscription: The subscription to delete
        """

    async def filter(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: UserId | None = None,
        birthing_person_id: UserId | None = None,
    ) -> list[Subscription]:
        """
        Filter subscriptions based on inputs.

        Args:
            labour_id: An optional Labour ID
            subscriber_id: An optional Subscriber ID
            birthing_person_id: An optional Birthing Person ID

        Returns:
            A list of subscriptions
        """

    async def filter_one_or_none(
        self,
        labour_id: LabourId | None = None,
        subscriber_id: UserId | None = None,
        birthing_person_id: UserId | None = None,
    ) -> Subscription | None:
        """
        Filter subscriptions based on inputs.

        Args:
            labour_id: An optional Labour ID
            subscriber_id: An optional Subscriber ID
            birthing_person_id: An optional Birthing Person ID

        Returns:
            A subscription if found, else returns None
        """

    async def get_by_id(self, subscription_id: SubscriptionId) -> Subscription | None:
        """
        Retrieve a subscription by ID.

        Args:
            subscription_id: The ID of the subscription to retrieve

        Returns:
            The subscription if found, else returns None
        """

    async def get_by_ids(self, subscription_ids: list[SubscriptionId]) -> list[Subscription]:
        """
        Retrieve a list of subscriptions by IDs.

        Args:
            subscription_ids: The IDs of the subscriptions to retrieve

        Returns:
            A list of subscriptions
        """
