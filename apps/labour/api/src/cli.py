import argparse
import logging

import uvloop
from dishka import AsyncContainer

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.infrastructure.persistence.initialize_mapping import map_all
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


async def publish_domain_events() -> None:
    """Fetches and publishes un-published domain events."""
    log.info("Starting domain event publish CLI command.")
    container_manager = await _setup_container()

    async with container_manager() as request_container:
        domain_event_publisher = await request_container.get(
            DomainEventPublisher, component=ComponentEnum.DEFAULT
        )
        await domain_event_publisher.publish_batch()

    await container_manager.close()
    log.info("CLI command finished.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fern Labour Labour Service CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    publish_domain_events_parser = subparsers.add_parser(
        "publish-domain-events", help="Fetches and publishes un-published domain events"
    )
    publish_domain_events_parser.set_defaults(func=publish_domain_events)

    args = parser.parse_args()

    async_func_kwargs = {k: v for k, v in vars(args).items() if k not in ["command", "func"]}

    if hasattr(args, "func"):
        uvloop.run(args.func(**async_func_kwargs))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
