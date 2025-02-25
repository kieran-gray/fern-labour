import logging

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.domain.subscription.enums import ContactMethod

log = logging.getLogger(__name__)


class ContactService:
    def __init__(
        self,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
        contact_email: str,
    ):
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service
        self._contact_email = contact_email

    def _generate_email(self, email: str, name: str, message: str) -> Notification:
        subject = f"Contact us submission from: {email}"
        data = {"email": email, "name": name, "message": message}
        message = self._email_generation_service.generate("contact_us_submission.html", data)
        return Notification(
            type=ContactMethod.EMAIL,
            destination=self._contact_email,
            message=message,
            subject=subject,
        )

    async def send_contact_email(
        self, email: str, name: str, message: str, user_id: str | None = None
    ) -> None:
        # TODO store message
        log.info(f"Contact us submission for email = {email} Userid = {user_id}")
        notification = self._generate_email(email=email, name=name, message=message)
        await self._notification_service.send(notification)
