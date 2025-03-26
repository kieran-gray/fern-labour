from enum import StrEnum
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from app.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.application.notifications.notification_service import NotificationService
from app.domain.labour.exceptions import InvalidLabourId, InvalidLabourUpdateId
from app.domain.notification.enums import NotificationStatus
from app.domain.notification.exceptions import (
    InvalidNotificationId,
    InvalidNotificationStatus,
    NotificationNotFoundById,
)
from app.domain.notification.repository import NotificationRepository
from app.domain.notification.vo_notification_id import NotificationId
from app.domain.subscription.enums import ContactMethod
from app.domain.subscription.exceptions import InvalidContactMethod


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(success=True, status=NotificationStatus.SENT)


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(success=True, status=NotificationStatus.SENT)


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
    notification_repo: NotificationRepository,
) -> NotificationService:
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    return NotificationService(
        email_notification_gateway=email_notification_gateway,
        sms_notification_gateway=sms_notification_gateway,
        notification_repository=notification_repo,
    )


async def test_can_create_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=ContactMethod.EMAIL.value,
        destination="test",
        template="template.html",
        data={"test": "test"},
    )
    assert notification
    assert notification.status == NotificationStatus.CREATED.value
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.CREATED


async def test_cannot_create_notification_invalid_labour_id(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidLabourId):
        await notification_service.create_notification(
            type=ContactMethod.EMAIL.value,
            destination="test",
            template="template.html",
            data={"test": "test"},
            labour_id="test",
        )


async def test_cannot_create_notification_invalid_labour_update_id(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidLabourUpdateId):
        await notification_service.create_notification(
            type=ContactMethod.EMAIL.value,
            destination="test",
            template="template.html",
            data={"test": "test"},
            labour_update_id="test",
        )


async def test_cannot_create_notification_invalid_contact_method(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidContactMethod):
        await notification_service.create_notification(
            type="fail",
            destination="test",
            template="template.html",
            data={"test": "test"},
        )


async def test_cannot_create_notification_invalid_notification_status(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationStatus):
        await notification_service.create_notification(
            type=ContactMethod.SMS.value,
            destination="test",
            template="template.html",
            data={"test": "test"},
            status="fail",
        )


async def test_can_update_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=ContactMethod.EMAIL.value,
        destination="test",
        template="template.html",
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
        type=ContactMethod.EMAIL.value,
        destination="test",
        template="template.html",
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
        type=ContactMethod.EMAIL.value,
        destination="test",
        template="template.html",
        data={"test": "test"},
    )
    await notification_service.send(notification)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.type is ContactMethod.EMAIL

    assert notification_service._sms_notification_gateway.sent_notifications == []
    assert notification_service._email_notification_gateway.sent_notifications == [notification]


async def test_can_send_sms(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        type=ContactMethod.SMS.value,
        destination="test",
        template="template.html",
        data={"test": "test"},
    )
    await notification_service.send(notification)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.type is ContactMethod.SMS

    assert notification_service._sms_notification_gateway.sent_notifications == [notification]
    assert notification_service._email_notification_gateway.sent_notifications == []


async def test_invalid_type_raises_error(
    notification_service: NotificationService,
) -> None:
    class ContactMethod(StrEnum):
        TEST = "test"

    notification: NotificationDTO = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED,
        type=ContactMethod.TEST,
        destination="dest",
        template="template.html",
        data={"test": "test"},
    )
    with pytest.raises(InvalidContactMethod):
        await notification_service.send(notification)


async def test_invalid_type_raises_not_implemented(
    notification_service: NotificationService,
) -> None:
    class ContactMethod(StrEnum):
        TEST = "test"

    with pytest.raises(NotImplementedError):
        await notification_service._get_notification_gateway(ContactMethod.TEST)
