from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import ContactUsData, LabourBegunData

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_router import NotificationRouter
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
)
from src.notification.domain.exceptions import (
    CannotResendNotification,
    InvalidNotificationChannel,
    InvalidNotificationId,
    InvalidNotificationStatus,
    InvalidNotificationTemplate,
    NotificationNotFoundById,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId
from tests.unit.app.application.conftest import MockSMSNotificationGateway


@pytest_asyncio.fixture
async def notification_service(
    notification_router: NotificationRouter,
    notification_generation_service: NotificationGenerationService,
    notification_repo: NotificationRepository,
) -> NotificationService:
    return NotificationService(
        notification_router=notification_router,
        notification_generation_service=notification_generation_service,
        notification_repository=notification_repo,
        event_producer=AsyncMock(),
    )


def get_notification(
    notification_service: NotificationService, channel: str
) -> NotificationDTO | None:
    gateway = notification_service._notification_router.get_gateway(channel)
    try:
        return gateway.sent_notifications[0]
    except IndexError:
        return None


async def test_can_create_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
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


async def test_cannot_create_notification_invalid_notification_channel(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationChannel):
        await notification_service.create_notification(
            channel="fail",
            destination="test",
            template="labour_update",
            data={"test": "test"},
        )


async def test_cannot_create_notification_invalid_notification_status(
    notification_service: NotificationService,
) -> None:
    with pytest.raises(InvalidNotificationStatus):
        await notification_service.create_notification(
            channel=NotificationChannel.SMS.value,
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
            channel=NotificationChannel.SMS.value,
            destination="test",
            template="invalid",
            data={"test": "test"},
        )


async def test_can_send_email(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
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
    assert stored_notification.channel is NotificationChannel.EMAIL

    assert get_notification(notification_service, NotificationChannel.SMS.value) is None
    sent_email = get_notification(notification_service, NotificationChannel.EMAIL.value)
    assert sent_email.destination == notification.destination
    assert sent_email.data == notification.data

    assert sent_email.id == notification.id
    assert sent_email.channel == notification.channel
    assert sent_email.template == notification.template
    assert sent_email.metadata == notification.metadata

    assert sent_email.subject != notification.subject
    assert sent_email.message != notification.message
    assert sent_email.external_id != stored_notification.external_id


async def test_can_send_sms(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.channel is NotificationChannel.SMS

    sent_sms = get_notification(notification_service, NotificationChannel.SMS.value)
    assert get_notification(notification_service, NotificationChannel.EMAIL.value) is None

    assert sent_sms.destination == notification.destination
    assert sent_sms.data == notification.data

    assert sent_sms.id == notification.id
    assert sent_sms.channel == notification.channel
    assert sent_sms.template == notification.template
    assert sent_sms.metadata == notification.metadata

    assert sent_sms.external_id != stored_notification.external_id
    assert sent_sms.message != notification.message


async def test_can_send_whatsapp(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.WHATSAPP.value,
        destination="whatsapp:+44123123123",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification
    assert stored_notification.status is NotificationStatus.SENT
    assert stored_notification.channel is NotificationChannel.WHATSAPP

    sent_whatsapp = get_notification(notification_service, NotificationChannel.WHATSAPP.value)

    assert sent_whatsapp.destination == notification.destination
    assert sent_whatsapp.destination.startswith("whatsapp")
    assert sent_whatsapp.data == notification.data

    assert sent_whatsapp.id == notification.id
    assert sent_whatsapp.channel == notification.channel
    assert sent_whatsapp.template == notification.template
    assert sent_whatsapp.metadata == notification.metadata

    assert sent_whatsapp.external_id != stored_notification.external_id
    assert sent_whatsapp.message != notification.message


async def test_cannot_send_with_invalid_id(notification_service: NotificationService) -> None:
    with pytest.raises(InvalidNotificationId):
        await notification_service.send(notification_id="invalid")


async def test_cannot_send_with_non_found_id(notification_service: NotificationService) -> None:
    with pytest.raises(NotificationNotFoundById):
        await notification_service.send(notification_id=str(uuid4()))


async def test_can_resend_unsent_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.resend(notification_id=notification.id)


async def test_can_resend_failed_notification(notification_service: NotificationService) -> None:
    class FailSMSGateway:
        sent_notifications = []

        async def send(self, data: NotificationDTO) -> NotificationSendResult:
            self.sent_notifications.append(data)
            return NotificationSendResult(
                success=False, status=NotificationStatus.FAILURE, external_id="TESTSMS"
            )

    notification_service._notification_router.register_gateway(
        channel=NotificationChannel.SMS, gateway=FailSMSGateway()
    )

    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    sent_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert sent_notification.status is NotificationStatus.FAILURE

    notification_service._notification_router.register_gateway(
        channel=NotificationChannel.SMS, gateway=MockSMSNotificationGateway()
    )
    await notification_service.resend(notification_id=notification.id)
    sent_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert sent_notification.status is NotificationStatus.SENT


async def test_can_resend_success_notification(notification_service: NotificationService) -> None:
    class SuccessSMSGateway:
        sent_notifications = []

        async def send(self, data: NotificationDTO) -> NotificationSendResult:
            self.sent_notifications.append(data)
            return NotificationSendResult(
                success=False, status=NotificationStatus.SUCCESS, external_id="TESTSMS"
            )

    notification_service._notification_router.register_gateway(
        channel=NotificationChannel.SMS, gateway=SuccessSMSGateway()
    )

    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)
    sent_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert sent_notification.status is NotificationStatus.SUCCESS
    with pytest.raises(CannotResendNotification):
        await notification_service.resend(notification_id=notification.id)


async def test_cannot_resend_sent_notification(notification_service: NotificationService) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="John Jones",
            birthing_person_first_name="John",
            subscriber_first_name="Jane",
            link="abc123",
        ).to_dict(),
        metadata={"test": "abc", "more_data": "test123"},
    )
    await notification_service.send(notification_id=notification.id)

    with pytest.raises(CannotResendNotification):
        await notification_service.resend(notification_id=notification.id)


async def test_cannot_resend_with_invalid_id(notification_service: NotificationService) -> None:
    with pytest.raises(InvalidNotificationId):
        await notification_service.resend(notification_id="invalid")


async def test_cannot_resend_with_non_found_id(notification_service: NotificationService) -> None:
    with pytest.raises(NotificationNotFoundById):
        await notification_service.resend(notification_id=str(uuid4()))
