import logging
from typing import Protocol
from uuid import UUID

from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import BaseNotificationData
from fern_labour_notifications_shared.template_data_mapping import TEMPLATE_TO_PAYLOAD

from src.notification.application.dtos.notification import NotificationContent
from src.notification.application.interfaces.template_engine import (
    EmailTemplateEngine,
    SMSTemplateEngine,
    WhatsAppTemplateEngine,
)
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.exceptions import (
    InvalidNotificationId,
    InvalidNotificationTemplate,
    NotificationNotFoundById,
    NotificationProcessingError,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId

log = logging.getLogger(__name__)


class NotificationContentGenerator(Protocol):
    def __call__(
        self, template: NotificationTemplate, data: BaseNotificationData
    ) -> NotificationContent: ...


class NotificationGenerationService:
    """
    Generates the content (subject, message) for a notification record.
    """

    def __init__(
        self,
        notification_repo: NotificationRepository,
        email_template_engine: EmailTemplateEngine,
        sms_template_engine: SMSTemplateEngine,
        whatsapp_template_engine: WhatsAppTemplateEngine,
    ):
        self._notification_repository = notification_repo
        self._email_template_engine = email_template_engine
        self._sms_template_engine = sms_template_engine
        self._whatsapp_template_engine = whatsapp_template_engine

    async def generate_content(self, notification_id: str) -> NotificationContent:
        try:
            notification_domain_id = NotificationId(UUID(notification_id))
        except ValueError:
            raise InvalidNotificationId(notification_id=notification_id)

        notification = await self._notification_repository.get_by_id(notification_domain_id)
        if not notification:
            raise NotificationNotFoundById(notification_id=notification_id)

        try:
            template = NotificationTemplate(notification.template)
        except ValueError:
            raise InvalidNotificationTemplate(notification.template)

        payload_data_type = self._get_payload_type(template=template)

        try:
            data = payload_data_type.from_dict(notification.data)
        except KeyError:
            raise NotificationProcessingError(
                f"Failed to convert data to payload data type for notification {notification_id}"
            )
        notification_content_generator = self._get_notification_content_generator(
            notification.channel
        )
        generated_content = notification_content_generator(template=template, data=data)
        log.info(
            f"Successfully generated {notification.channel.value} content for {notification_id}"
        )
        return generated_content

    def _get_payload_type(self, template: NotificationTemplate) -> type[BaseNotificationData]:
        """Gets the required data payload type for the given template."""
        payload_type = TEMPLATE_TO_PAYLOAD.get(template)
        if not payload_type:
            raise NotificationProcessingError(f"No payload data type found for template {template}")
        return payload_type

    def _generate_email(
        self, template: NotificationTemplate, data: BaseNotificationData
    ) -> NotificationContent:
        subject = self._email_template_engine.generate_subject(template_name=template, data=data)
        message = self._email_template_engine.generate_message(template_name=template, data=data)
        return NotificationContent(message=message, subject=subject)

    def _generate_sms(
        self, template: NotificationTemplate, data: BaseNotificationData
    ) -> NotificationContent:
        message = self._sms_template_engine.generate_message(template_name=template, data=data)
        return NotificationContent(message=message)

    def _generate_whatsapp(
        self, template: NotificationTemplate, data: BaseNotificationData
    ) -> NotificationContent:
        subject = self._whatsapp_template_engine.generate_subject(template_name=template, data=data)
        message = self._whatsapp_template_engine.generate_message(template_name=template, data=data)
        return NotificationContent(message=message, subject=subject)

    def _get_notification_content_generator(
        self, channel: NotificationChannel
    ) -> NotificationContentGenerator:
        if channel is NotificationChannel.EMAIL:
            return self._generate_email
        if channel is NotificationChannel.SMS:
            return self._generate_sms
        if channel is NotificationChannel.WHATSAPP:
            return self._generate_whatsapp
