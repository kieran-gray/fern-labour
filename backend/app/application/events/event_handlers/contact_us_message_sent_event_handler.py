import logging
from typing import Any

from app.application.events.event_handler import EventHandler
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.domain.subscription.enums import ContactMethod

log = logging.getLogger(__name__)


class ContactUsMessageSentEventHandler(EventHandler):
    def __init__(
        self,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
        contact_email: str,
    ):
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service
        self._contact_email = contact_email

    def _generate_email(self, data: dict[str, Any]) -> Notification:
        subject = f"Contact us submission from: {data["email"]}"
        message = self._email_generation_service.generate("contact_us_submission.html", data)
        return Notification(
            type=ContactMethod.EMAIL,
            destination=self._contact_email,
            message=message,
            subject=subject,
        )

    async def handle(self, event: dict[str, Any]) -> None:
        log.info(
            "Contact us submission for email = %s Userid = %s",
            event["data"]["email"],
            event["data"]["user_id"],
        )
        notification = self._generate_email(event["data"])
        await self._notification_service.send(notification)
