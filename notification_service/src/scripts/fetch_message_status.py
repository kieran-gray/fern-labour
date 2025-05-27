import asyncio
import logging

from src.core.infrastructure.persistence.initialize_mapping import map_all
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.setup.app_factory import create_dishka_container
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.logs import configure_logging
from src.setup.settings import Settings

configure_logging()
log = logging.getLogger(__name__)


async def main() -> None:
    settings: Settings = Settings.from_file()
    container = create_dishka_container(settings=settings)

    map_all()

    async with container() as request_container:
        notification_delivery_service = await request_container.get(
            NotificationDeliveryService, component=ComponentEnum.NOTIFICATIONS
        )
        await update_delivery_status(notification_delivery_service=notification_delivery_service)

    await container.close()


async def update_delivery_status(
    notification_delivery_service: NotificationDeliveryService,
) -> None:
    log.info("Starting notification delivery status update")
    await notification_delivery_service.update_undelivered_notification_delivery_status()
    log.info("Notification delivery status update complete")


if __name__ == "__main__":
    asyncio.run(main())
