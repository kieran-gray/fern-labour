import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.events import NotificationRequested
from fern_labour_notifications_shared.notification_data import SubscriberApprovedData

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.domain.domain_event.repository import DomainEventRepository
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
        domain_event_repository: DomainEventRepository,
        domain_event_publisher: DomainEventPublisher,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._domain_event_repository = domain_event_repository
        self._domain_event_publisher = domain_event_publisher
        self._tracking_link = tracking_link
        self._template = NotificationTemplate.SUBSCRIBER_APPROVED

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
        notification_event = NotificationRequested.create(
            aggregate_type="subscription",
            aggregate_id=domain_event.data["subscription_id"],
            data={
                "channel": ContactMethod.EMAIL.value,
                "destination": subscriber.destination(ContactMethod.EMAIL),
                "template": self._template.value,
                "data": notification_data.to_dict(),
                "metadata": notification_metadata.to_dict(),
            },
        )
        await self._domain_event_repository.save(domain_event=notification_event)

        await self._domain_event_repository.commit()

        try:
            await self._domain_event_publisher.publish_batch()
        except Exception as err:
            log.error(f"Error creating background publishing job: {err}")
