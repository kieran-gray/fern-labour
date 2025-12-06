import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_notifications_shared.enums import NotificationPriority
from fern_labour_notifications_shared.event_data import NotificationRequestedData
from fern_labour_notifications_shared.notification_data import SubscriberApprovedData

from src.core.application.notification_service_client import NotificationServiceClient
from src.subscription.domain.enums import ContactMethod
from src.user.application.dtos.user import UserDTO
from src.user.application.services.user_query_service import UserQueryService

log = logging.getLogger(__name__)


@dataclass
class SubscriberApprovedNotificationMetadata:
    labour_id: str
    subscription_id: str
    from_user_id: str
    to_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "labour_id": self.labour_id,
            "subscription_id": self.subscription_id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
        }


class SubscriberApprovedEventHandler(EventHandler):
    def __init__(
        self,
        user_service: UserQueryService,
        notification_service_client: NotificationServiceClient,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._notification_service_client = notification_service_client
        self._tracking_link = tracking_link

    def _generate_notification_data(
        self, birthing_person: UserDTO, subscriber: UserDTO
    ) -> SubscriberApprovedData:
        return SubscriberApprovedData(
            subscriber_first_name=subscriber.first_name,
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            link=self._tracking_link,
        )

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)

        birthing_person = await self._user_service.get(
            user_id=domain_event.data["birthing_person_id"]
        )
        subscriber = await self._user_service.get(user_id=domain_event.data["subscriber_id"])

        notification_data = self._generate_notification_data(birthing_person, subscriber)
        notification_metadata = SubscriberApprovedNotificationMetadata(
            labour_id=domain_event.data["labour_id"],
            subscription_id=domain_event.data["subscription_id"],
            from_user_id=birthing_person.id,
            to_user_id=subscriber.id,
        )

        notification_request = NotificationRequestedData(
            channel=ContactMethod.EMAIL,
            destination=subscriber.destination(ContactMethod.EMAIL),
            template_data=notification_data,
            metadata=notification_metadata.to_dict(),
            priority=NotificationPriority.NORMAL,
        )

        await self._notification_service_client.request_notification(notification_request)
