import json
from typing import Any
import emails
from dataclasses import dataclass

from app.application.interfaces.notfication_gateway import NotificationGateway
from app.setup.settings import Settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def generate_email(data: dict[str, Any]) -> EmailData:
    return EmailData(html_content=json.dumps(data), subject="TEST 123456")


class EmailNotificationGateway(NotificationGateway):
    """Notification gateway that sends emails"""

    def __init__(self, settings: Settings):
        self._settings = settings

    def send(self, data: dict[str, Any]) -> None:
        email_settings = self._settings.notification.email
        assert email_settings.emails_enabled

        email_data = generate_email(data)

        message = emails.Message(
            subject=email_data.subject,
            html=email_data.html_content,
            mail_from=(email_settings.emails_from_name, email_settings.emails_from_email),
        )
        smtp_options = {"host": email_settings.smtp_host, "port": email_settings.smtp_port}
        if email_settings.smtp_tls:
            smtp_options["tls"] = True
        elif email_settings.smtp_ssl:
            smtp_options["ssl"] = True
        if email_settings.smtp_user:
            smtp_options["user"] = email_settings.smtp_user
        if email_settings.smtp_password:
            smtp_options["password"] = email_settings.smtp_password
        message.send(to="test123@example.com", smtp=smtp_options)
