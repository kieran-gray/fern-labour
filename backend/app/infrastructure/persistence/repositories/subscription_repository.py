from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.vo_subscription_id import SubscriptionId
from app.domain.user.vo_user_id import UserId
from app.infrastructure.persistence.tables.subscriptions import subscriptions_table


class SQLAlchemySubscriptionRepository(SubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

        """Repository interface for Subscription entity"""

    async def save(self, subscription: Subscription) -> None:
        """
        Save or update a subscription.

        Args:
            subscription: The subscription to save
        """
        self._session.add(subscription)
        await self._session.commit()

    async def delete(self, subscription: Subscription) -> None:
        """
        Delete a subscription.

        Args:
            subscription: The subscription to delete
        """
        await self._session.delete(subscription)
        await self._session.commit()

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
        stmt = select(Subscription)
        if labour_id:
            stmt = stmt.where(subscriptions_table.c.labour_id == labour_id.value)
        if subscriber_id:
            stmt = stmt.where(subscriptions_table.c.subscriber_id == subscriber_id.value)
        if birthing_person_id:
            stmt = stmt.where(subscriptions_table.c.birthing_person_id == birthing_person_id.value)

        result = await self._session.execute(stmt)
        return list(result.scalars())

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
        stmt = select(Subscription)
        if labour_id:
            stmt = stmt.where(subscriptions_table.c.labour_id == labour_id.value)
        if subscriber_id:
            stmt = stmt.where(subscriptions_table.c.subscriber_id == subscriber_id.value)
        if birthing_person_id:
            stmt = stmt.where(subscriptions_table.c.birthing_person_id == birthing_person_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, subscription_id: SubscriptionId) -> Subscription | None:
        """
        Retrieve a subscription by ID.

        Args:
            subscription_id: The ID of the subscription to retrieve

        Returns:
            The subscription if found, else returns None
        """
        stmt = select(Subscription).where(subscriptions_table.c.id == subscription_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids(self, subscription_ids: list[SubscriptionId]) -> list[Subscription]:
        """
        Retrieve a list of subscriptions by IDs.

        Args:
            subscription_ids: The IDs of the subscriptions to retrieve

        Returns:
            A list of subscriptions
        """
        stmt = select(Subscription).where(
            subscriptions_table.c.id.in_([s.value for s in subscription_ids])
        )

        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def get_active_subscriptions_for_labour(self, labour_id: LabourId) -> list[Subscription]:
        """
        Retrieve a list of active subscriptions by IDs.

        Args:
            labour_id: The Labour ID to fetch the subscriptions for

        Returns:
            A list of subscriptions
        """
        stmt = select(Subscription).where(
            (
                subscriptions_table.c.labour_id == labour_id.value,
                subscriptions_table.c.status == SubscriptionStatus.SUBSCRIBED.value,
            )
        )
        result = await self._session.execute(stmt)
        return list(result.scalars())
