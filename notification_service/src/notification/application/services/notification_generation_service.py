import logging
from typing import Protocol
from uuid import UUID

from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import BaseNotificationData
from fern_labour_notifications_shared.template_data_mapping import TEMPLATE_TO_PAYLOAD

from src.notification.application.dtos.notification import NotificationContent
from src.notification.application.exceptions import (
    CannotGenerateNotificationContent,
)
from src.notification.application.interfaces.template_engine import (
    NotificationTemplateEngine,
)
from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.exceptions import (
    InvalidNotificationChannel,
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

    def __init__(self, notification_repo: NotificationRepository):
        self._notification_repository = notification_repo
        self._engines: dict[NotificationChannel, NotificationTemplateEngine] = {}

    def _channel_to_domain(self, channel: str) -> NotificationChannel:
        try:
            notification_channel = NotificationChannel(channel)
        except ValueError:
            raise InvalidNotificationChannel(notification_channel=channel)
        return notification_channel

    async def _get_notification(self, notification_id: str) -> Notification:
        try:
            notification_domain_id = NotificationId(UUID(notification_id))
        except ValueError:
            raise InvalidNotificationId(notification_id=notification_id)

        notification = await self._notification_repository.get_by_id(notification_domain_id)
        if not notification:
            raise NotificationNotFoundById(notification_id=notification_id)
        return notification

    def register_template_engine(
        self, channel: str, template_engine: NotificationTemplateEngine
    ) -> None:
        """Register a template engine for a specific channel"""
        notification_channel = self._channel_to_domain(channel=channel)
        self._engines[notification_channel] = template_engine

    async def generate_content(
        self, notification_id: str | None = None, notification: Notification | None = None
    ) -> NotificationContent:
        if not notification and not notification_id:
            raise CannotGenerateNotificationContent(
                message="Must provide one of `notification` or `notification_id`"
            )

        if not notification and notification_id:
            notification = await self._get_notification(notification_id=notification_id)

        assert notification

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
        template_engine = self._get_template_engine(notification.channel)
        generated_content = self._generate(
            template_engine=template_engine, template=template, data=data
        )
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

    def _generate(
        self,
        template_engine: NotificationTemplateEngine,
        template: NotificationTemplate,
        data: BaseNotificationData,
    ) -> NotificationContent:
        subject = None
        try:
            subject = template_engine.generate_subject(template_name=template, data=data)
        except NotImplementedError:
            pass
        message = template_engine.generate_message(template_name=template, data=data)
        return NotificationContent(message=message, subject=subject)

    def _get_template_engine(self, channel: NotificationChannel) -> NotificationTemplateEngine:
        if template_engine := self._engines.get(channel):
            return template_engine
        raise NotImplementedError(f"Template engine for channel {channel} not implemented")
