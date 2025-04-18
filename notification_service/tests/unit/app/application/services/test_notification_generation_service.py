from uuid import uuid4

import pytest
import pytest_asyncio

from src.notification.application.dtos.notification import NotificationContent, NotificationDTO
from src.notification.application.dtos.notification_data import ContactUsData
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import NotificationTemplate, NotificationType
from src.notification.domain.exceptions import (
    InvalidNotificationId,
    NotificationNotFoundById,
    NotificationProcessingError,
)


@pytest_asyncio.fixture
async def notification(notification_service: NotificationService) -> NotificationDTO:
    return await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )


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
        type=NotificationType.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data={"test": "test"},
    )
    with pytest.raises(NotificationProcessingError):
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
