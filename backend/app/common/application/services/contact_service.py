import logging

from app.notification.application.dtos.notification import NotificationContent
from app.notification.application.dtos.notification_data import ContactUsData
from app.notification.application.services.notification_service import NotificationService
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from app.notification.domain.enums import NotificationTemplate
from app.subscription.domain.enums import ContactMethod

log = logging.getLogger(__name__)


class ContactService:
    def __init__(
        self,
        notification_service: NotificationService,
        email_template_engine: EmailTemplateEngine,
        contact_email: str,
    ):
        self._notification_service = notification_service
        self._email_template_engine = email_template_engine
        self._contact_email = contact_email
        self._template = NotificationTemplate.CONTACT_US_SUBMISSION

    def _generate_notification_data(
        self, email: str, name: str, message: str, user_id: str | None = None
    ) -> ContactUsData:
        return ContactUsData(email=email, name=name, message=message, user_id=user_id or "")

    def _generate_email(self, data: ContactUsData) -> NotificationContent:
        subject = f"Contact us submission from: {data.email}"
        message = self._email_template_engine.generate_message(self._template, data)
        return NotificationContent(message=message, subject=subject)

    async def send_contact_email(
        self, email: str, name: str, message: str, user_id: str | None = None
    ) -> None:
        log.info(f"Contact us submission for email = {email} Userid = {user_id}")
        notification_data = self._generate_notification_data(
            email=email, name=name, message=message, user_id=user_id
        )
        notification_content = self._generate_email(data=notification_data)
        notification = await self._notification_service.create_notification(
            type=ContactMethod.EMAIL.value,
            destination=self._contact_email,
            template=self._template.value,
            data=notification_data.to_dict(),
            from_user_id=user_id,
        )
        notification.add_notification_content(content=notification_content)
        await self._notification_service.send(notification)
