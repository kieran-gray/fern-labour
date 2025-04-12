import logging
from dataclasses import dataclass
from typing import Any

from app.common.application.event_handler import EventHandler
from app.common.domain.event import DomainEvent
from app.common.domain.producer import EventProducer
from app.notification.application.dtos.notification_data import LabourUpdateData
from app.notification.domain.enums import NotificationTemplate
from app.notification.domain.events import NotificationRequested
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.user.application.dtos.user import UserDTO
from app.user.application.services.user_query_service import UserQueryService
from app.user.domain.exceptions import UserNotFoundById

log = logging.getLogger(__name__)


@dataclass
class LabourCompletedNotificationMetadata:
    labour_id: str
    from_user_id: str
    to_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "labour_id": self.labour_id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
        }


class LabourCompletedEventHandler(EventHandler):
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
        self._template = NotificationTemplate.LABOUR_UPDATE

    def _generate_notification_data(
        self,
        birthing_person: UserDTO,
        subscriber: UserDTO,
        notes: str,
    ) -> LabourUpdateData:
        update = f"{birthing_person.first_name} has completed labour!"
        if notes:
            update += f"\n\nThey added the following note:\n\n{notes}"
        return LabourUpdateData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            subscriber_first_name=subscriber.first_name,
            update=update,
            link=self._tracking_link,
            notes=notes,
        )

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)
        birthing_person_id = domain_event.data["birthing_person_id"]
        labour_id = domain_event.data["labour_id"]

        birthing_person = await self._user_service.get(user_id=birthing_person_id)
        subscriptions = await self._subscription_query_service.get_labour_subscriptions(
            requester_id=birthing_person_id, labour_id=labour_id
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
                    notes=domain_event.data["notes"],
                )
                notification_metadata = LabourCompletedNotificationMetadata(
                    labour_id=subscription.labour_id,
                    from_user_id=subscription.birthing_person_id,
                    to_user_id=subscriber.id,
                )
                notification_event = NotificationRequested.create(
                    data={
                        "type": method,
                        "destination": destination,
                        "template": self._template.value,
                        "data": notification_data.to_dict(),
                        "metadata": notification_metadata.to_dict(),
                    }
                )
                await self._event_producer.publish(event=notification_event)
