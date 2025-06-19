from uuid import UUID

import pytest
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import ContactUsData, LabourBegunData

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import NotificationGateway
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
)
from src.notification.domain.exceptions import (
    InvalidNotificationStatus,
    NotificationNotFoundByExternalId,
)
from src.notification.domain.value_objects.notification_id import NotificationId


async def test_status_callback_updates_status(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
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
    await notification_delivery_service.delivery_status_callback(
        external_id=stored_notification.external_id, status=NotificationStatus.SUCCESS
    )
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SUCCESS


async def test_status_callback_error_invalid_status(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
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
        await notification_delivery_service.delivery_status_callback(
            external_id=stored_notification.external_id, status="invalid"
        )


async def test_status_callback_error_external_id_not_found(
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    with pytest.raises(NotificationNotFoundByExternalId):
        await notification_delivery_service.delivery_status_callback(
            external_id="fail", status=NotificationStatus.SENT
        )


async def test_update_undelivered_notification_delivery_status_for_email_raises_not_implemented(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    with pytest.raises(NotImplementedError):
        await notification_delivery_service.update_undelivered_notification_delivery_status()


async def test_update_undelivered_notification_delivery_status(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.SMS.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="test",
            birthing_person_first_name="test",
            subscriber_first_name="test",
            link="test",
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT

    await notification_delivery_service.update_undelivered_notification_delivery_status()
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SUCCESS


async def test_update_undelivered_notification_delivery_status_unchanged(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.WHATSAPP.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="test",
            birthing_person_first_name="test",
            subscriber_first_name="test",
            link="test",
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT

    await notification_delivery_service.update_undelivered_notification_delivery_status()
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT


async def test_update_undelivered_notification_delivery_status_none(
    notification_service: NotificationService,
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    notification = await notification_service.create_notification(
        channel=NotificationChannel.WHATSAPP.value,
        destination="test",
        template=NotificationTemplate.LABOUR_BEGUN.value,
        data=LabourBegunData(
            birthing_person_name="test",
            birthing_person_first_name="test",
            subscriber_first_name="test",
            link="test",
        ).to_dict(),
    )
    await notification_service.send(notification_id=notification.id)
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT

    class MockGateway(NotificationGateway):
        sent_notifications = []

        async def send(self, data: NotificationDTO) -> NotificationSendResult:
            self.sent_notifications.append(data)
            return NotificationSendResult(
                success=True, status=NotificationStatus.SENT, external_id="TESTWHATSAPP"
            )

        async def get_status(self, external_id: str) -> str | None:
            return None

        async def redact_notification_body(self, external_id: str) -> None:
            return None

    notification_delivery_service._notification_router.register_gateway(
        channel=NotificationChannel.WHATSAPP.value, gateway=MockGateway()
    )

    await notification_delivery_service.update_undelivered_notification_delivery_status()
    stored_notification = await notification_service._notification_repository.get_by_id(
        notification_id=NotificationId(UUID(notification.id))
    )
    assert stored_notification.status is NotificationStatus.SENT
