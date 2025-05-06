import json

import pytest
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import (
    LabourAnnouncementData,
    SubscriberInviteData,
)

from src.notification.domain.exceptions import GenerationTemplateNotFound
from src.notification.infrastructure.template_engines.whatsapp_template_engine import (
    WhatsAppTemplateEngine,
)


def test_can_generate_whatsapp() -> None:
    engine = WhatsAppTemplateEngine()
    data = LabourAnnouncementData(
        birthing_person_name="test lastname",
        birthing_person_first_name="test",
        subscriber_first_name="test2",
        announcement="test3",
        link="https://test.com",
    )
    subject = engine.generate_subject(
        template_name=NotificationTemplate.LABOUR_ANNOUNCEMENT, data=data
    )
    message = engine.generate_message(
        template_name=NotificationTemplate.LABOUR_ANNOUNCEMENT, data=data
    )
    assert isinstance(subject, str)
    assert subject.startswith("HX")

    assert isinstance(message, str)
    message_dict = json.loads(message)
    assert message_dict["1"] == "test2"
    assert message_dict["2"] == "test lastname"
    assert message_dict["3"] == "test3"


def test_cannot_generate_whatsapp_subject_for_not_implemented_template() -> None:
    engine = WhatsAppTemplateEngine()
    data = SubscriberInviteData(subscriber_name="test2", link="https://test.com")
    with pytest.raises(GenerationTemplateNotFound):
        engine.generate_subject(template_name=NotificationTemplate.SUBSCRIBER_INVITE, data=data)


def test_cannot_generate_whatsapp_message_for_not_implemented_template() -> None:
    engine = WhatsAppTemplateEngine()
    data = SubscriberInviteData(subscriber_name="test2", link="https://test.com")
    with pytest.raises(GenerationTemplateNotFound):
        engine.generate_message(template_name=NotificationTemplate.SUBSCRIBER_INVITE, data=data)
