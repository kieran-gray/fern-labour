import logging
from dataclasses import dataclass
from typing import Any

import httpx
from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_notifications_shared.enums import NotificationPriority
from fern_labour_notifications_shared.event_data import NotificationRequestedData
from fern_labour_notifications_shared.notification_data import LabourAnnouncementData

from src.labour.domain.labour_update.enums import LabourUpdateType
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.domain.enums import SubscriptionAccessLevel
from src.user.application.dtos.user import UserDTO
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.exceptions import UserNotFoundById

log = logging.getLogger(__name__)

NOTIFICATION_SERVICE_URL = "http://host.docker.internal:8001/api/v1/notification"


@dataclass
class LabourUpdatePostedNotificationMetadata:
    labour_id: str
    from_user_id: str
    to_user_id: str
    labour_update_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "labour_id": self.labour_id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "labour_update_id": self.labour_update_id,
        }


class LabourUpdatePostedEventHandler(EventHandler):
    def __init__(
        self,
        user_service: UserQueryService,
        subscription_query_service: SubscriptionQueryService,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._subscription_query_service = subscription_query_service
        self._tracking_link = tracking_link

    def _generate_notification_data(
        self,
        birthing_person: UserDTO,
        subscriber: UserDTO,
        announcement: str,
    ) -> LabourAnnouncementData:
        return LabourAnnouncementData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            birthing_person_first_name=birthing_person.first_name,
            subscriber_first_name=subscriber.first_name,
            announcement=announcement,
            link=self._tracking_link,
        )

    async def _send_notifications(
        self, event: DomainEvent
    ) -> list[NotificationRequestedData]:
        birthing_person_id = event.data["birthing_person_id"]
        labour_id = event.data["labour_id"]
        labour_update_id = event.data["labour_update_id"]

        birthing_person = await self._user_service.get(user_id=birthing_person_id)

        subscriptions = await self._subscription_query_service.get_labour_subscriptions(
            requester_id=birthing_person_id,
            labour_id=labour_id,
            access_level=SubscriptionAccessLevel.SUPPORTER.value,
        )

        notifications = []

        async with httpx.AsyncClient() as client:
            for subscription in subscriptions:
                try:
                    subscriber = await self._user_service.get(user_id=subscription.subscriber_id)
                except UserNotFoundById as err:
                    log.error(err)
                    continue

                for method in subscription.contact_methods:
                    destination = subscriber.destination(method)
                    if not destination:
                        continue

                    notification_data = self._generate_notification_data(
                        birthing_person=birthing_person,
                        subscriber=subscriber,
                        announcement=event.data["message"],
                    )
                    notification_metadata = LabourUpdatePostedNotificationMetadata(
                        labour_id=subscription.labour_id,
                        from_user_id=subscription.birthing_person_id,
                        to_user_id=subscriber.id,
                        labour_update_id=labour_update_id,
                    )

                    notification_request = NotificationRequestedData(
                        channel=method,
                        destination=destination,
                        template_data=notification_data,
                        metadata=notification_metadata.to_dict(),
                        priority=NotificationPriority.NORMAL,
                    )

                    try:
                        log.info(
                            f"Attempting to send notification to {NOTIFICATION_SERVICE_URL} "
                            f"for {destination} via {method}"
                        )
                        response = await client.post(
                            NOTIFICATION_SERVICE_URL,
                            json=notification_request.to_dict(),
                            timeout=10.0,
                        )
                        response.raise_for_status()
                        log.info(
                            f"Notification sent successfully to {destination} via {method}"
                        )
                        notifications.append(notification_request)
                    except httpx.ConnectError as err:
                        log.error(
                            f"Connection error sending notification to {destination} via {method}: {err}. "
                            f"Is the notification service running at {NOTIFICATION_SERVICE_URL}?"
                        )
                    except httpx.HTTPStatusError as err:
                        log.error(
                            f"HTTP error {err.response.status_code} sending notification to {destination} "
                            f"via {method}: {err.response.text}"
                        )
                    except httpx.HTTPError as err:
                        log.error(
                            f"Failed to send notification to {destination} via {method}: {err}"
                        )

        return notifications

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)
        if domain_event.data["labour_update_type"] != LabourUpdateType.ANNOUNCEMENT.value:
            return

        try:
            await self._send_notifications(event=domain_event)
        except Exception as err:
            log.error(f"Error sending notifications: {err}")
