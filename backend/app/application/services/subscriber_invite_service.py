import logging

from app.application.dtos.user import UserDTO
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
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

    def _generate_email(self, subscriber: UserDTO, destination: str) -> Notification:
        subject = "A Brilliant Way to Share Your Baby Journey! 🍼"

        email_data = {
            "subscriber_name": f"{subscriber.first_name} {subscriber.last_name}",
            "link": "https://fernlabour.com",
        }
        message = self._email_generation_service.generate("subscriber_invite.html", email_data)
        return Notification(
            type=ContactMethod.EMAIL, destination=destination, message=message, subject=subject
        )

    async def send_invite(self, subscriber_id: str, invite_email: str) -> None:
        subscriber = await self._user_service.get(subscriber_id)

        notification = self._generate_email(subscriber=subscriber, destination=invite_email)

        await self._notification_service.send(notification)
