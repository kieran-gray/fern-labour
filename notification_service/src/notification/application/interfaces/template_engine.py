from typing import Protocol

from src.notification.application.dtos.notification_data import BaseNotificationData
from src.notification.domain.enums import NotificationTemplate


class NotificationTemplateEngine(Protocol):
    """Abstract Base Class for a notification template engine."""

    def generate_subject(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a subject string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """

    def generate_message(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a message string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """


class EmailTemplateEngine(NotificationTemplateEngine, Protocol): ...


class SMSTemplateEngine(NotificationTemplateEngine, Protocol): ...


class WhatsAppTemplateEngine(NotificationTemplateEngine, Protocol): ...
