import logging
from typing import Protocol
from uuid import UUID

from app.notification.application.dtos.notification import NotificationContent
from app.notification.application.dtos.notification_data import (
    BaseNotificationData,
    ContactUsData,
    LabourInviteData,
    LabourUpdateData,
    SubscriberInviteData,
)
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from app.notification.application.template_engines.sms_template_engine import SMSTemplateEngine
from app.notification.domain.enums import NotificationTemplate, NotificationType
from app.notification.domain.exceptions import (
    InvalidNotificationId,
    InvalidNotificationTemplate,
    NotificationNotFoundById,
    NotificationProcessingError,
)
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.value_objects.notification_id import NotificationId

log = logging.getLogger(__name__)


TEMPLATE_TO_PAYLOAD: dict[NotificationTemplate, type[BaseNotificationData]] = {
    NotificationTemplate.LABOUR_UPDATE: LabourUpdateData,
    NotificationTemplate.LABOUR_INVITE: LabourInviteData,
    NotificationTemplate.SUBSCRIBER_INVITE: SubscriberInviteData,
    NotificationTemplate.CONTACT_US_SUBMISSION: ContactUsData,
}


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
    ):
        self._notification_repository = notification_repo
        self._email_template_engine = email_template_engine
        self._sms_template_engine = sms_template_engine

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
            raise InvalidNotificationTemplate(template=notification.template)

        payload_data_type = self._get_payload_type(template)

        try:
            data = payload_data_type.from_dict(notification.data)
        except KeyError:
            raise NotificationProcessingError(
                f"Failed to convert data to payload data type for notification {notification_id}"
            )

        notification_content_generator = self._get_notification_content_generator(notification.type)
        generated_content = notification_content_generator(template=template, data=data)
        log.info(f"Successfully generated {notification.type.value} content for {notification_id}")
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

    def _get_notification_content_generator(
        self, notification_type: NotificationType
    ) -> NotificationContentGenerator:
        if notification_type is NotificationType.EMAIL:
            return self._generate_email
        if notification_type is NotificationType.SMS:
            return self._generate_sms
        raise NotImplementedError(f"Notification generator for {notification_type} not implemented")
