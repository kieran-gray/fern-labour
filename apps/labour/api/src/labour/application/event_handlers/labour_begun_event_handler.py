import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_notifications_shared.enums import NotificationPriority
from fern_labour_notifications_shared.event_data import NotificationRequestedData
from fern_labour_notifications_shared.notification_data import LabourBegunData

from src.core.application.notification_service_client import NotificationServiceClient
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.domain.enums import SubscriptionAccessLevel
from src.user.application.dtos.user import UserDTO
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.exceptions import UserNotFoundById

log = logging.getLogger(__name__)

@dataclass
class LabourBegunNotificationMetadata:
    labour_id: str
    from_user_id: str
    to_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "labour_id": self.labour_id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
        }


class LabourBegunEventHandler(EventHandler):
    def __init__(
        self,
        user_service: UserQueryService,
        subscription_query_service: SubscriptionQueryService,
        notification_service_client: NotificationServiceClient,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._subscription_query_service = subscription_query_service
        self._notification_service_client = notification_service_client
        self._tracking_link = tracking_link

    def _generate_notification_data(
        self, birthing_person: UserDTO, subscriber: UserDTO
    ) -> LabourBegunData:
        return LabourBegunData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            birthing_person_first_name=birthing_person.first_name,
            subscriber_first_name=subscriber.first_name,
            link=self._tracking_link,
        )

    async def _send_notifications(
        self, event: DomainEvent
    ) -> list[NotificationRequestedData]:
        birthing_person_id = event.data["birthing_person_id"]
        labour_id = event.data["labour_id"]

        birthing_person = await self._user_service.get(user_id=birthing_person_id)

        subscriptions = await self._subscription_query_service.get_labour_subscriptions(
            requester_id=birthing_person_id,
            labour_id=labour_id,
            access_level=SubscriptionAccessLevel.SUPPORTER.value,
        )

        for subscription in subscriptions:
            try:
                subscriber = await self._user_service.get(subscription.subscriber_id)
            except UserNotFoundById as err:
                log.error(err)
                continue

            for method in subscription.contact_methods:
                destination = subscriber.destination(method)
                if not destination:
                    continue

                notification_data = self._generate_notification_data(
                    birthing_person, subscriber
                )
                notification_metadata = LabourBegunNotificationMetadata(
                    labour_id=subscription.labour_id,
                    from_user_id=subscription.birthing_person_id,
                    to_user_id=subscriber.id,
                )

                notification_request = NotificationRequestedData(
                    channel=method,
                    destination=destination,
                    template_data=notification_data,
                    metadata=notification_metadata.to_dict(),
                    priority=NotificationPriority.HIGH,
                )

                await self._notification_service_client.request_notification(notification_request)

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)

        await self._send_notifications(event=domain_event)