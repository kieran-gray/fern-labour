import logging

from app.application.dtos.notification import NotificationContent
from app.application.dtos.user import UserDTO
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_data import SubscriberInviteData
from app.application.notifications.notification_service import NotificationService
from app.application.services.user_service import UserService
from app.domain.subscription.enums import ContactMethod

log = logging.getLogger(__name__)


class SubscriberInviteService:
    def __init__(
        self,
        user_service: UserService,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ):
        self._user_service = user_service
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service
        self._template = "subscriber_invite.html"

    def _generate_notification_data(self, subscriber: UserDTO) -> SubscriberInviteData:
        return SubscriberInviteData(
            subscriber_name=f"{subscriber.first_name} {subscriber.last_name}",
            link="https://fernlabour.com",
        )

    def _generate_email(self, data: SubscriberInviteData) -> NotificationContent:
        subject = "A Brilliant Way to Share Your Baby Journey! 🍼"
        message = self._email_generation_service.generate(self._template, data.to_dict())
        return NotificationContent(message=message, subject=subject)

    async def send_invite(self, subscriber_id: str, invite_email: str) -> None:
        subscriber = await self._user_service.get(subscriber_id)

        notification_data = self._generate_notification_data(subscriber=subscriber)
        notification_content = self._generate_email(data=notification_data)
        notification = await self._notification_service.create_notification(
            type=ContactMethod.EMAIL.value,
            destination=invite_email,
            template=self._template,
            data=notification_data.to_dict(),
            to_user_id=subscriber_id,
        )
        notification.add_notification_content(notification_content)
        await self._notification_service.send(notification)
