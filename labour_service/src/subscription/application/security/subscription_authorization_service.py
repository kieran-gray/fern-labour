import logging
from uuid import UUID

from src.labour.domain.labour.exceptions import InvalidLabourId, UnauthorizedLabourRequest
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    UnauthorizedSubscriptionRequest,
    UnauthorizedSubscriptionUpdateRequest,
)
from src.subscription.domain.repository import SubscriptionRepository
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class SubscriptionAuthorizationService:
    """
    Centralized service for handling authorization rules related to Subscriptions.
    Methods raise specific Unauthorized exceptions if the check fails.
    """

    def __init__(self, subscription_repository: SubscriptionRepository):
        self._subscription_repository = subscription_repository

    async def ensure_can_view_subscription(
        self, requester_id: str, subscription: Subscription
    ) -> None:
        """
        Checks if the requester can view the details of a specific subscription.
        Rule: Requester must be the subscriber or the birthing person.
        """
        user_id = self._to_user_id(user_id=requester_id)
        is_subscriber = subscription.subscriber_id == user_id
        is_birthing_person = subscription.birthing_person_id == user_id

        if not (is_subscriber or is_birthing_person):
            log.warning(
                f"User {requester_id} unauthorized to view subscription {subscription.id_.value}"
            )
            raise UnauthorizedSubscriptionRequest()

        if is_subscriber and subscription.status is not SubscriptionStatus.SUBSCRIBED:
            log.warning(
                f"Subscriber {requester_id} unauthorized to view "
                f"non-active subscription {subscription.id_.value}"
            )
            raise UnauthorizedSubscriptionRequest()

    async def ensure_can_manage_as_birthing_person(
        self, requester_id: str, subscription: Subscription
    ) -> None:
        """
        Checks if the requester can perform management actions as the birthing person
        on this subscription (e.g., remove, block, update role).
        Rule: Requester must be the birthing person associated with the subscription.
        """
        user_id = self._to_user_id(user_id=requester_id)
        if subscription.birthing_person_id != user_id:
            log.warning(
                f"User {requester_id} unauthorized to manage subscription {subscription.id_.value} "
                f"as birthing person ({subscription.birthing_person_id})"
            )
            raise UnauthorizedSubscriptionUpdateRequest()

    async def ensure_can_manage_as_subscriber(
        self, requester_id: str, subscription: Subscription
    ) -> None:
        """
        Checks if the requester can perform management actions as the subscriber
        on this subscription (e.g., update contact methods).
        Rule: Requester must be the subscriber associated with the subscription.
        """
        user_id = self._to_user_id(user_id=requester_id)
        if subscription.subscriber_id != user_id:
            log.warning(
                f"User {requester_id} unauthorized to manage subscription {subscription.id_.value} "
                f"as subscriber ({subscription.subscriber_id})"
            )
            raise UnauthorizedSubscriptionUpdateRequest()

    async def ensure_can_access_labour(self, requester_id: str, labour_id: str) -> None:
        """
        Checks if the user can access the labour via an active subscription.
        Rule: Requester has an active subscription.
        """
        subscription = await self._subscription_repository.filter_one_or_none(
            labour_id=self._to_labour_id(labour_id=labour_id),
            subscriber_id=self._to_user_id(user_id=requester_id),
            status=SubscriptionStatus.SUBSCRIBED,
        )

        if not subscription:
            log.warning(
                f"User {requester_id} unauthorized to access labour {labour_id} via subscription"
            )
            raise UnauthorizedLabourRequest()

    def _to_user_id(self, user_id: str) -> UserId:
        return UserId(user_id)

    def _to_labour_id(self, labour_id: str) -> LabourId:
        try:
            return LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()
