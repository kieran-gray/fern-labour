import json

from src.notification.application.dtos.notification_data import BaseNotificationData
from src.notification.application.interfaces.template_engine import (
    WhatsAppTemplateEngine as WhatsAppTemplateEngineInterface,
)
from src.notification.domain.enums import NotificationTemplate
from src.notification.domain.exceptions import GenerationTemplateNotFound
from src.notification.infrastructure.templates.whatsapp.message_templates import (
    TEMPLATE_TO_MESSAGE_CONTENT_VARIABLES,
    TEMPLATE_TO_TWILIO_TEMPLATE_SID,
)


class WhatsAppTemplateEngine(WhatsAppTemplateEngineInterface):
    def generate_subject(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a subject string from a template.
        We are going to use this to store the message template SID.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template.
        """
        template_sid = TEMPLATE_TO_TWILIO_TEMPLATE_SID.get(template_name)
        if not template_sid:
            raise GenerationTemplateNotFound(template=template_name.value)
        return template_sid

    def generate_message(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a message html string from a template.
        We are going to use this to store the the template content variables as a JSON string.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        content_variables_template = TEMPLATE_TO_MESSAGE_CONTENT_VARIABLES.get(template_name)
        if not content_variables_template:
            raise GenerationTemplateNotFound(template=template_name.value)
        content = {key: getattr(data, attr, "") for key, attr in content_variables_template.items()}
        return json.dumps(content)
