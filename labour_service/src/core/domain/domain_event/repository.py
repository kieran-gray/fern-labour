from typing import Protocol

from fern_labour_core.events.event import DomainEvent


class DomainEventRepository(Protocol):
    """Repository interface for Domain Events"""

    async def commit(self) -> None:
        """
        Commit changes to the aggregate.
        """

    async def save(self, domain_event: DomainEvent) -> None:
        """
        Save or update a domain event.

        Args:
            domain_event: The domain event to save
        """

    async def save_many(self, domain_events: list[DomainEvent]) -> None:
        """
        Save or update a lsit of domain events.

        Args:
            domain_events: The list of domain events to save
        """

    async def get_unpublished(self, limit: int = 100) -> list[DomainEvent]:
        """
        Get a list of unpublished domain events.
        """

    async def mark_as_published(self, domain_event_id: str) -> None:
        """
        Mark a domain event as published.

        Args:
            domain_event_id: The id of the domain event to mark as published
        """

    async def mark_many_as_published(self, domain_event_ids: list[str]) -> None:
        """
        Mark a list of domain events as published.

        Args:
            domain_event_ids: The list of domain event ids to mark as published
        """
