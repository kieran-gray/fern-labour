from datetime import UTC, datetime

from fern_labour_core.events.event import DomainEvent
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.domain_event.repository import DomainEventRepository
from src.core.infrastructure.persistence.domain_event.table import domain_events_table


class SQLAlchemyDomainEventRepository(DomainEventRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        """
        Commit changes to the aggregate.
        """
        await self._session.commit()

    async def save(self, domain_event: DomainEvent) -> None:
        """
        Save or update a domain event.

        Args:
            domain_event: The domain event to save
        """
        self._session.add(domain_event)

    async def save_many(self, domain_events: list[DomainEvent]) -> None:
        """
        Save or update a lsit of domain events.

        Args:
            domain_events: The list of domain events to save
        """
        for domain_event in domain_events:
            self._session.add(domain_event)

    async def get_unpublished(self, limit: int = 100) -> list[DomainEvent]:
        """
        Get a list of unpublished domain events.
        """
        stmt = (
            select(DomainEvent)
            .where(domain_events_table.c.published_at.is_(None))
            .with_for_update(skip_locked=True)
            .limit(limit=limit)
        )

        result = await self._session.execute(stmt)

        return list(result.scalars())

    async def mark_as_published(self, domain_event_id: str) -> None:
        """
        Mark a domain event as published.

        Args:
            domain_event_id: The id of the domain event to mark as published
        """
        stmt = (
            update(domain_events_table)
            .where(domain_events_table.c.event_id == domain_event_id)
            .values(published_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def mark_many_as_published(self, domain_event_ids: list[str]) -> None:
        """
        Mark a list of domain events as published.

        Args:
            domain_event_ids: The list of domain event ids to mark as published
        """
        stmt = (
            update(domain_events_table)
            .where(domain_events_table.c.event_id.in_(domain_event_ids))
            .values(published_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)
