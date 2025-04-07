from pathlib import Path

from jinja2 import Template

from app.notification.application.dtos.notification_data import BaseNotificationData
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from app.notification.domain.enums import NotificationTemplate
from app.notification.domain.exceptions import GenerationTemplateNotFound
from app.notification.infrastructure.notifications.email.templates.subject_templates import (
    TEMPLATE_TO_SUBJECT_STRING_TEMPLATE,
)


class Jinja2EmailTemplateEngine(EmailTemplateEngine):
    def __init__(self) -> None:
        self.directory = Path(__file__).parent / "templates" / "build"

    def generate_subject(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a subject string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        subject_template = TEMPLATE_TO_SUBJECT_STRING_TEMPLATE.get(template_name)
        if not subject_template:
            raise GenerationTemplateNotFound(template=template_name.value)
        return subject_template.format(**data.to_dict())

    def generate_message(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        """
        Generate a message html string from a template.

        Args:
            template: The name of the template to use for generation
            data: The data to add to the template
        """
        template_str = self.directory.joinpath(f"{template_name}.html").read_text()
        template: Template = Template(template_str)
        html_content = template.render(data.to_dict())
        return html_content
