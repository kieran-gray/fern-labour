from app.notification.application.dtos.notification_data import BaseNotificationData
from app.notification.application.template_engines.sms_template_engine import (
    SMSTemplateEngine as SMSTemplateEngineInterface,
)
from app.notification.domain.enums import NotificationTemplate
from app.notification.domain.exceptions import GenerationTemplateNotFound
from app.notification.infrastructure.notifications.sms.templates.message_templates import (
    TEMPLATE_TO_MESSAGE_STRING_TEMPLATE,
)


class SMSTemplateEngine(SMSTemplateEngineInterface):
    def generate_subject(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a subject string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        raise NotImplementedError()

    def generate_message(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a message html string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        message_template = TEMPLATE_TO_MESSAGE_STRING_TEMPLATE.get(template_name)
        if not message_template:
            raise GenerationTemplateNotFound(template=template_name.value)
        return message_template.format(**data.to_dict())
