from enum import StrEnum
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from app.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.notification.application.dtos.notification_data import ContactUsData
from app.notification.application.gateways.email_notification_gateway import (
    EmailNotificationGateway,
)
from app.notification.application.gateways.sms_notification_gateway import SMSNotificationGateway
from app.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from app.notification.application.services.notification_service import NotificationService
from app.notification.domain.enums import NotificationStatus, NotificationTemplate, NotificationType
from app.notification.domain.exceptions import (
    InvalidNotificationId,
    InvalidNotificationStatus,
    InvalidNotificationTemplate,
    InvalidNotificationType,
    NotificationNotFoundByExternalId,
    NotificationNotFoundById,
)
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.value_objects.notification_id import NotificationId


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id="TEST123"
        )


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id="TESTABC"
        )


@pytest_asyncio.fixture
def email_notification_gateway():
    return MockEmailNotificationGateway()


@pytest_asyncio.fixture
def sms_notification_gateway():
    return MockSMSNotificationGateway()


@pytest_asyncio.fixture
async def notification_service(
    email_notification_gateway: EmailNotificationGateway,
    sms_notification_gateway: SMSNotificationGateway,
    notification_generation_service: NotificationGenerationService,
    notification_repo: NotificationRepository,
) -> NotificationService:
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    return NotificationService(
        email_notification_gateway=email_notification_gateway,
        sms_notification_gateway=sms_notification_gateway,
        notification_generation_service=notification_generation_service,
        notification_repository=notification_repo,
    )


async def test_can_create_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template="labour_update",
        data={"test": "test"},
    )
    assert notification
    assert notification.status == NotificationStatus.CREATED.value
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.CREATED


async def test_cannot_create_notification_invalid_notification_type(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationType):
        await notification_service.create_notification(
            type="fail",
            destination="test",
            template="labour_update",
            data={"test": "test"},
        )


async def test_cannot_create_notification_invalid_notification_status(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationStatus):
        await notification_service.create_notification(
            type=NotificationType.SMS.value,
            destination="test",
            template="labour_update",
            data={"test": "test"},
            status="fail",
        )


async def test_cannot_create_notification_invalid_template(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationTemplate):
        await notification_service.create_notification(
            type=NotificationType.SMS.value,
            destination="test",
            template="invalid",
            data={"test": "test"},
        )


async def test_can_update_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template="labour_update",
        data={"test": "test"},
    )
    notification = await notification_service.update_notification(
        notification_id=notification.id, status=NotificationStatus.SENT
    )
    assert notification.status == NotificationStatus.SENT.value


async def test_can_update_notification_with_external_id(
    notification_service: NotificationService,
) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template="labour_update",
        data={"test": "test"},
    )
    notification = await notification_service.update_notification(
        notification_id=notification.id, status=NotificationStatus.SENT, external_id="test"
    )
    assert notification.status == NotificationStatus.SENT.value
    assert notification.external_id == "test"


async def test_cannot_update_notification_invalid_notification_id(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationId):
        await notification_service.update_notification(
            notification_id="test", status=NotificationStatus.SENT
        )


async def test_cannot_update_notification_invalid_notification_status(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationStatus):
        await notification_service.update_notification(notification_id=str(uuid4()), status="fail")


async def test_cannot_update_notification_notification_not_found(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(NotificationNotFoundById):
        await notification_service.update_notification(
            notification_id=str(uuid4()), status=NotificationStatus.SENT
        )


async def test_can_send_email(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.type is NotificationType.EMAIL

    assert notification_service._sms_notification_gateway.sent_notifications == []
    sent_email = notification_service._email_notification_gateway.sent_notifications[0]
    assert sent_email.destination == notification.destination
    assert sent_email.data == notification.data

    assert sent_email.id == notification.id
    assert sent_email.type == notification.type
    assert sent_email.template == notification.template
    assert sent_email.metadata == notification.metadata

    assert sent_email.subject != notification.subject
    assert sent_email.message != notification.message
    assert sent_email.external_id != stored_notification.external_id


async def test_can_send_sms(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.SMS.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.type is NotificationType.SMS

    sent_sms = notification_service._sms_notification_gateway.sent_notifications[0]
    assert notification_service._email_notification_gateway.sent_notifications == []

    assert sent_sms.destination == notification.destination
    assert sent_sms.data == notification.data

    assert sent_sms.id == notification.id
    assert sent_sms.type == notification.type
    assert sent_sms.template == notification.template
    assert sent_sms.metadata == notification.metadata

    assert sent_sms.external_id != stored_notification.external_id
    assert sent_sms.message != notification.message


async def test_cannot_send_with_invalid_id(notification_service: NotificationService) -> None:
    with pytest.raises(InvalidNotificationId):
        await notification_service.send(notification_id="invalid")


async def test_cannot_send_with_non_found_id(notification_service: NotificationService) -> None:
    with pytest.raises(NotificationNotFoundById):
        await notification_service.send(notification_id=str(uuid4()))


async def test_invalid_type_raises_not_implemented(
    notification_service: NotificationService,
) -> None:
    class NotificationType(StrEnum):
        TEST = "test"

    with pytest.raises(NotImplementedError):
        await notification_service._get_notification_gateway(NotificationType.TEST)


async def test_status_callback_updates_status(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT
    await notification_service.status_callback(
        external_id=stored_notification.external_id, status=NotificationStatus.SUCCESS
    )
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SUCCESS


async def test_status_callback_error_invalid_status(
    notification_service: NotificationService,
) -> None:
    notification = await notification_service.create_notification(
        type=NotificationType.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT
    with pytest.raises(InvalidNotificationStatus):
        await notification_service.status_callback(
            external_id=stored_notification.external_id, status="invalid"
        )


async def test_status_callback_error_external_id_not_found(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(NotificationNotFoundByExternalId):
        await notification_service.status_callback(
            external_id="fail", status=NotificationStatus.SENT
        )
