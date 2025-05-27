from unittest.mock import AsyncMock
from uuid import UUID

import pytest
import pytest_asyncio
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import ContactUsData, LabourBegunData

from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.application.services.notification_router import NotificationRouter
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
)
from src.notification.domain.exceptions import (
    InvalidNotificationStatus,
    NotificationNotFoundByExternalId,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId


@pytest_asyncio.fixture
async def notification_delivery_service(
    notification_service: NotificationService,
    notification_repo: NotificationRepository,
    notification_router: NotificationRouter,
) -> NotificationDeliveryService:
    return NotificationDeliveryService(
        notification_service=notification_service,
        notification_router=notification_router,
        notification_repository=notification_repo,
        event_producer=AsyncMock(),
    )


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
