from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import ContactUsData

from src.notification.application.dtos.notification import NotificationContent, NotificationDTO
from src.notification.application.exceptions import CannotGenerateNotificationContent
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.exceptions import (
    InvalidNotificationChannel,
    InvalidNotificationId,
    InvalidNotificationTemplate,
    NotificationNotFoundById,
    NotificationProcessingError,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId
from src.notification.infrastructure.template_engines.sms_template_engine import SMSTemplateEngine
from tests.unit.app.application.conftest import MockEmailTemplateEngine


@pytest_asyncio.fixture
async def notification(notification_service: NotificationService) -> NotificationDTO:
    return await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )


async def test_can_register_template_engine(
    notification_repo: NotificationRepository,
) -> NotificationGenerationService:
    notification_generation_service = NotificationGenerationService(
        notification_repo=notification_repo,
    )
    email_template_engine = MockEmailTemplateEngine()
    notification_generation_service.register_template_engine(
        channel=NotificationChannel.EMAIL, template_engine=email_template_engine
    )
    assert notification_generation_service._engines


async def test_cannot_register_template_engine_invalid_channel(
    notification_repo: NotificationRepository,
) -> NotificationGenerationService:
    notification_generation_service = NotificationGenerationService(
        notification_repo=notification_repo,
    )
    email_template_engine = MockEmailTemplateEngine()
    with pytest.raises(InvalidNotificationChannel):
        notification_generation_service.register_template_engine(
            channel="test", template_engine=email_template_engine
        )


async def test_channel_missing_engine_raises_not_implmemented_error(
    notification_repo: NotificationRepository,
    notification: NotificationDTO,
) -> NotificationGenerationService:
    notification_generation_service = NotificationGenerationService(
        notification_repo=notification_repo,
    )
    sms_template_engine = SMSTemplateEngine()
    notification_generation_service.register_template_engine(
        channel=NotificationChannel.SMS, template_engine=sms_template_engine
    )
    with pytest.raises(NotImplementedError):
        await notification_generation_service.generate_content(notification.id)


async def test_can_generate_notification_content(
    notification_generation_service: NotificationGenerationService,
    notification: NotificationDTO,
) -> None:
    notification_content = await notification_generation_service.generate_content(notification.id)
    assert notification_content
    assert isinstance(notification_content, NotificationContent)
    assert notification_content.subject
    assert notification_content.message


async def test_cannot_generate_notification_content_invalid_id(
    notification_generation_service: NotificationGenerationService,
) -> None:
    with pytest.raises(InvalidNotificationId):
        await notification_generation_service.generate_content("invalid")


async def test_cannot_generate_notification_content_notification_not_found(
    notification_generation_service: NotificationGenerationService,
) -> None:
    with pytest.raises(NotificationNotFoundById):
        await notification_generation_service.generate_content(str(uuid4()))


async def test_cannot_generate_notification_content_invalid_data(
    notification_generation_service: NotificationGenerationService,
    notification_service: NotificationService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data={"test": "test"},
    )
    with pytest.raises(NotificationProcessingError):
        await notification_generation_service.generate_content(notification.id)


async def test_cannot_generate_notification_content_invalid_template(
    notification_generation_service: NotificationGenerationService,
    notification: NotificationDTO,
) -> None:
    notification_id = NotificationId(UUID(notification.id))
    domain_notification = await notification_generation_service._notification_repository.get_by_id(
        notification_id
    )
    domain_notification.template = "test"
    await notification_generation_service._notification_repository.save(domain_notification)

    with pytest.raises(InvalidNotificationTemplate):
        await notification_generation_service.generate_content(notification.id)


async def test_cannot_generate_notification_not_payload_dataclass(
    notification_generation_service: NotificationGenerationService,
    notification: NotificationDTO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_template_mapping = {}
    monkeypatch.setattr(
        "src.notification.application.services.notification_generation_service.TEMPLATE_TO_PAYLOAD",
        mock_template_mapping,
    )
    with pytest.raises(NotificationProcessingError):
        await notification_generation_service.generate_content(notification.id)


async def test_cannot_generate_notification_no_args(
    notification_generation_service: NotificationGenerationService,
) -> None:
    with pytest.raises(CannotGenerateNotificationContent):
        await notification_generation_service.generate_content()
