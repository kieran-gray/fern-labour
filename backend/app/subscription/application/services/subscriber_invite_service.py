import logging
from dataclasses import dataclass

from app.notification.application.dtos.notification_data import SubscriberInviteData
from app.notification.application.services.notification_service import NotificationService
from app.notification.domain.enums import NotificationTemplate
from app.subscription.domain.enums import ContactMethod
from app.user.application.dtos.user import UserDTO
from app.user.application.services.user_service import UserService

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
        user_service: UserService,
        notification_service: NotificationService,
    ):
        self._user_service = user_service
        self._notification_service = notification_service
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
        notification = await self._notification_service.create_notification(
            type=ContactMethod.EMAIL.value,
            destination=invite_email,
            template=self._template.value,
            data=notification_data.to_dict(),
            metadata=notification_metadata.to_dict(),
        )
        await self._notification_service.send(notification_id=notification.id)
