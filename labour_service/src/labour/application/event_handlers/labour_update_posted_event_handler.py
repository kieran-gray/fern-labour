import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_core.events.producer import EventProducer
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.events import NotificationRequested
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
        event_producer: EventProducer,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._subscription_query_service = subscription_query_service
        self._event_producer = event_producer
        self._tracking_link = tracking_link
        self._template = NotificationTemplate.LABOUR_ANNOUNCEMENT

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

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)
        if domain_event.data["labour_update_type"] == LabourUpdateType.STATUS_UPDATE.value:
            return

        birthing_person_id = domain_event.data["birthing_person_id"]
        labour_id = domain_event.data["labour_id"]
        labour_update_id = domain_event.data["labour_update_id"]

        birthing_person = await self._user_service.get(user_id=birthing_person_id)

        subscriptions = await self._subscription_query_service.get_labour_subscriptions(
            requester_id=birthing_person_id,
            labour_id=labour_id,
            access_level=SubscriptionAccessLevel.SUPPORTER.value,
        )

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
                    announcement=domain_event.data["message"],
                )
                notification_metadata = LabourUpdatePostedNotificationMetadata(
                    labour_id=subscription.labour_id,
                    from_user_id=subscription.birthing_person_id,
                    to_user_id=subscriber.id,
                    labour_update_id=labour_update_id,
                )
                notification_event = NotificationRequested.create(
                    data={
                        "channel": method,
                        "destination": destination,
                        "template": self._template.value,
                        "data": notification_data.to_dict(),
                        "metadata": notification_metadata.to_dict(),
                    }
                )
                await self._event_producer.publish(event=notification_event)
