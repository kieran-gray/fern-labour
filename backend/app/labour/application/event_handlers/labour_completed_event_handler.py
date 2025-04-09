import logging
from dataclasses import dataclass
from typing import Any, Protocol

from app.common.application.event_handler import EventHandler
from app.common.domain.event import DomainEvent
from app.notification.application.dtos.notification import NotificationContent
from app.notification.application.dtos.notification_data import LabourUpdateData
from app.notification.application.services.notification_service import NotificationService
from app.notification.domain.enums import NotificationTemplate
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.domain.enums import ContactMethod
from app.user.application.dtos.user import UserDTO
from app.user.application.services.user_service import UserService
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


class LabourCompletedNotificationGenerator(Protocol):
    def __call__(self, data: LabourUpdateData) -> NotificationContent: ...


class LabourCompletedEventHandler(EventHandler):
    def __init__(
        self,
        user_service: UserService,
        subscription_query_service: SubscriptionQueryService,
        notification_service: NotificationService,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._subscription_query_service = subscription_query_service
        self._notification_service = notification_service
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
                notification = await self._notification_service.create_notification(
                    type=ContactMethod(method),
                    destination=destination,
                    template=self._template.value,
                    data=notification_data.to_dict(),
                    metadata=notification_metadata.to_dict(),
                )
                await self._notification_service.send(notification_id=notification.id)
