import pytest
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import (
    LabourUpdateData,
    SubscriberInviteData,
)

from src.notification.domain.exceptions import GenerationTemplateNotFound
from src.notification.infrastructure.template_engines.jinja2_email_template_engine import (
    Jinja2EmailTemplateEngine,
)
from src.notification.infrastructure.templates.email.subject_templates import (
    TEMPLATE_TO_SUBJECT_STRING_TEMPLATE,
)


def test_can_generate_email() -> None:
    engine = Jinja2EmailTemplateEngine()
    data = LabourUpdateData(
        birthing_person_name="test",
        subscriber_first_name="test2",
        update="test3",
        link="https://test.com",
    )
    subject = engine.generate_subject(template_name=NotificationTemplate.LABOUR_UPDATE, data=data)
    message = engine.generate_message(template_name=NotificationTemplate.LABOUR_UPDATE, data=data)

    assert isinstance(subject, str)
    assert isinstance(message, str)


def test_cannot_generate_sms_for_not_implemented_template(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = Jinja2EmailTemplateEngine()
    data = SubscriberInviteData(subscriber_name="test2", link="https://test.com")
    mock_template_mapping = TEMPLATE_TO_SUBJECT_STRING_TEMPLATE
    mock_template_mapping.pop(NotificationTemplate.SUBSCRIBER_INVITE)
    monkeypatch.setattr(
        "src.notification.infrastructure.templates.email.subject_templates.TEMPLATE_TO_SUBJECT_STRING_TEMPLATE",
        mock_template_mapping,
    )
    with pytest.raises(GenerationTemplateNotFound):
        engine.generate_subject(template_name=NotificationTemplate.SUBSCRIBER_INVITE, data=data)
