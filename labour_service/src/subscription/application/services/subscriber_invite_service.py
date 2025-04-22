import logging
from dataclasses import dataclass

from src.core.domain.producer import EventProducer
from src.notification.enums import NotificationTemplate
from src.notification.events import NotificationRequested
from src.notification.notification_data import SubscriberInviteData
from src.subscription.domain.enums import ContactMethod
from src.user.application.dtos.user import UserDTO
from src.user.application.services.user_query_service import UserQueryService

log = logging.getLogger(__name__)


@dataclass
class SubscriberInviteNotificationMetadata:
    from_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "from_user_id": self.from_user_id,
        }


class SubscriberInviteService:
    def __init__(
        self,
        user_service: UserQueryService,
        event_producer: EventProducer,
    ):
        self._user_service = user_service
        self._event_producer = event_producer
        self._template = NotificationTemplate.SUBSCRIBER_INVITE

    def _generate_notification_data(self, subscriber: UserDTO) -> SubscriberInviteData:
        return SubscriberInviteData(
            subscriber_name=f"{subscriber.first_name} {subscriber.last_name}",
            link="https://fernlabour.com",
        )

    async def send_invite(self, subscriber_id: str, invite_email: str) -> None:
        subscriber = await self._user_service.get(subscriber_id)

        notification_data = self._generate_notification_data(subscriber=subscriber)
        notification_metadata = SubscriberInviteNotificationMetadata(from_user_id=subscriber_id)
        notification_event = NotificationRequested.create(
            data={
                "type": ContactMethod.EMAIL.value,
                "destination": invite_email,
                "template": self._template.value,
                "data": notification_data.to_dict(),
                "metadata": notification_metadata.to_dict(),
            }
        )
        await self._event_producer.publish(event=notification_event)
