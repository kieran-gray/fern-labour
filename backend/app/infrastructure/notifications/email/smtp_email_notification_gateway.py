import logging
from typing import Any

import emails

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import EmailNotificationGateway

log = logging.getLogger(__name__)


class SMTPEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that sends emails"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        emails_from_email: str,
        smtp_tls: bool,
        smtp_ssl: bool,
        smtp_user: str | None = None,
        smtp_password: str | None = None,
        emails_from_name: str | None = None,
    ):
        self._smtp_host = smtp_host
        self._smtp_user = smtp_user
        self._smtp_password = smtp_password
        self._emails_from_email = emails_from_email
        self._emails_from_name = emails_from_name
        self._smtp_tls = smtp_tls
        self._smtp_ssl = smtp_ssl
        self._smtp_port = smtp_port

    async def send(self, notification: Notification) -> None:
        message = emails.Message(
            subject=notification.subject,
            html=notification.message,
            mail_from=(self._emails_from_name, self._emails_from_email),
        )
        smtp_options: dict[str, Any] = {"host": self._smtp_host, "port": self._smtp_port}
        if self._smtp_tls:
            smtp_options["tls"] = True
        elif self._smtp_ssl:
            smtp_options["ssl"] = True
        if self._smtp_user:
            smtp_options["user"] = self._smtp_user
        if self._smtp_password:
            smtp_options["password"] = self._smtp_password
        message.send(to=notification.destination, smtp=smtp_options)

        log.info("Sent email notification")
