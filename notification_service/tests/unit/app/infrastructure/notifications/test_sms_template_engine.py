import pytest
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import (
    LabourUpdateData,
    SubscriberInviteData,
)

from src.notification.domain.exceptions import GenerationTemplateNotFound
from src.notification.infrastructure.template_engines.sms_template_engine import SMSTemplateEngine


def test_can_generate_sms() -> None:
    engine = SMSTemplateEngine()
    data = LabourUpdateData(
        birthing_person_name="test",
        subscriber_first_name="test2",
        update="test3",
        link="https://test.com",
    )
    message = engine.generate_message(template_name=NotificationTemplate.LABOUR_UPDATE, data=data)
    assert isinstance(message, str)


def test_cannot_generate_sms_for_not_implemented_template() -> None:
    engine = SMSTemplateEngine()
    data = SubscriberInviteData(subscriber_name="test2", link="https://test.com")
    with pytest.raises(GenerationTemplateNotFound):
        engine.generate_message(template_name=NotificationTemplate.SUBSCRIBER_INVITE, data=data)


def test_generating_sms_subject_raises_exception() -> None:
    engine = SMSTemplateEngine()
    data = LabourUpdateData(
        birthing_person_name="test",
        subscriber_first_name="test2",
        update="test3",
        link="https://test.com",
    )
    with pytest.raises(NotImplementedError):
        engine.generate_subject(template_name=NotificationTemplate.LABOUR_UPDATE, data=data)
