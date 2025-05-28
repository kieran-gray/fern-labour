from typing import Protocol

from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import BaseNotificationData


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
