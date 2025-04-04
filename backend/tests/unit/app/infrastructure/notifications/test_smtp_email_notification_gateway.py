import logging
from unittest.mock import patch
from uuid import uuid4

from app.labour.domain.subscription.enums import ContactMethod
from app.notification.application.dtos.notification import NotificationDTO
from app.notification.domain.enums import NotificationStatus
from app.notification.infrastructure.notifications.email.smtp_email_notification_gateway import (
    SMTPEmailNotificationGateway,
)

MODULE = "app.notification.infrastructure.notifications.email.smtp_email_notification_gateway"


def test_smtp_email_notification_gateway_initialization():
    gateway = SMTPEmailNotificationGateway(
        smtp_host="smtp.example.com",
        smtp_port=587,
        emails_from_email="noreply@example.com",
        smtp_tls=True,
        smtp_ssl=False,
        smtp_user="user",
        smtp_password="password",
        emails_from_name="Example",
    )
    assert gateway._smtp_host == "smtp.example.com"
    assert gateway._smtp_port == 587
    assert gateway._emails_from_email == "noreply@example.com"
    assert gateway._smtp_tls is True
    assert gateway._smtp_ssl is False
    assert gateway._smtp_user == "user"
    assert gateway._smtp_password == "password"
    assert gateway._emails_from_name == "Example"


@patch("emails.Message.send")
async def test_send_email_notification(mock_send):
    mock_send.return_value = None

    gateway = SMTPEmailNotificationGateway(
        smtp_host="smtp.example.com",
        smtp_port=587,
        emails_from_email="noreply@example.com",
        smtp_tls=True,
        smtp_ssl=False,
        smtp_user="user",
        smtp_password="password",
        emails_from_name="Example",
    )
    notification = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED.value,
        type=ContactMethod.EMAIL.value,
        template="template.html",
        data={"test": "test"},
        destination="test@example.com",
    )

    await gateway.send(notification)

    mock_send.assert_called_once()
    smtp_options = {
        "host": "smtp.example.com",
        "port": 587,
        "tls": True,
        "user": "user",
        "password": "password",
    }
    _, kwargs = mock_send.call_args
    assert kwargs["to"] == "test@example.com"
    assert kwargs["smtp"] == smtp_options


@patch("emails.Message.send", side_effect=Exception("SMTP Error"))
async def test_send_email_notification_error(mock_send, caplog):  # noqa
    gateway = SMTPEmailNotificationGateway(
        smtp_host="smtp.example.com",
        smtp_port=587,
        emails_from_email="noreply@example.com",
        smtp_tls=False,
        smtp_ssl=True,
        smtp_user="user",
        smtp_password="password",
        emails_from_name="Example",
    )
    notification = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED.value,
        type=ContactMethod.EMAIL.value,
        template="template.html",
        data={"test": "test"},
        destination="test@example.com",
    )

    with caplog.at_level(logging.WARNING, logger=MODULE):
        await gateway.send(notification)
        assert len(caplog.records) == 1
        assert caplog.messages[0] == "Failed to send email notification"
