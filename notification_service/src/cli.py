import argparse
import asyncio
import logging

from dishka import AsyncContainer

from src.core.infrastructure.persistence.initialize_mapping import map_all
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.application.services.notification_service import NotificationService
from src.setup.app_factory import create_dishka_container
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.logs import configure_logging
from src.setup.settings import Settings

configure_logging()
log = logging.getLogger(__name__)


async def _setup_container() -> AsyncContainer:
    app_settings: Settings = Settings.from_file()

    container = create_dishka_container(settings=app_settings)
    map_all()

    return container


async def fetch_notification_status() -> None:
    """Fetches and updates the delivery status of undelivered notifications."""
    log.info("Starting notification delivery status update CLI command.")
    container_manager = await _setup_container()

    async with container_manager() as request_container:
        notification_delivery_service = await request_container.get(
            NotificationDeliveryService, component=ComponentEnum.NOTIFICATIONS
        )
        log.info("Calling application service to update statuses...")
        await notification_delivery_service.update_undelivered_notification_delivery_status()
        log.info("Notification delivery status update complete.")

    await container_manager.close()
    log.info("CLI command finished.")


async def resend_notification(notification_id: str) -> None:
    """Resends a failed or unsent notification."""
    log.info("Starting resend notification CLI command.")
    container_manager = await _setup_container()

    async with container_manager() as request_container:
        notification_service = await request_container.get(
            NotificationService, component=ComponentEnum.NOTIFICATIONS
        )
        log.info("Resending notification...")

        log.info("Resend notification command complete.")
        log.info("Calling application service to update statuses...")
        await notification_service.resend(notification_id=notification_id)
        log.info("Notification delivery status update complete.")

    await container_manager.close()
    log.info("CLI command finished.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fern Labour Notification Service CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    fetch_status = subparsers.add_parser(
        "fetch-status", help="Fetches and updates notification delivery statuses"
    )
    fetch_status.set_defaults(func=fetch_notification_status)

    resend_parser = subparsers.add_parser("resend", help="Resends an unsent or failed notification")
    resend_parser.add_argument(
        "--notification-id", "-n", type=str, help="ID of notification to resend."
    )
    resend_parser.set_defaults(func=resend_notification)

    args = parser.parse_args()

    async_func_kwargs = {k: v for k, v in vars(args).items() if k not in ["command", "func"]}

    if hasattr(args, "func"):
        asyncio.run(args.func(**async_func_kwargs))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
