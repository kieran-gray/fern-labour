import logging

from fern_labour_pub_sub.idempotency_store import (
    AlreadyCompletedError,
    IdempotencyStore,
    LockContentionError,
)
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.persistence.idempotency.table import (
    ProcessingStatus,
    consumer_processed_events_table,
)

log = logging.getLogger(__name__)


class SQLAlchemyIdempotencyStore(IdempotencyStore):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def try_claim_event(self, event_id: str) -> None:
        stmt_insert = (
            insert(consumer_processed_events_table)
            .values(event_id=event_id, status=ProcessingStatus.PROCESSING)
            .on_conflict_do_nothing()
        )

        await self._session.execute(stmt_insert)

        log.debug(f"Attempting to acquire lock for event: {event_id}")
        try:
            stmt_lock = (
                select(consumer_processed_events_table.c.status)
                .where(consumer_processed_events_table.c.event_id == event_id)
                .with_for_update(nowait=True)
            )
            result = await self._session.execute(stmt_lock)
            current_status = result.scalar_one()

            if current_status == ProcessingStatus.COMPLETED:
                raise AlreadyCompletedError(f"Event {event_id} already completed.")

            log.info(f"Lock acquired for event: {event_id}")

        except DBAPIError:
            # This error isn't necessarily caused by lock contention
            raise LockContentionError(f"Event {event_id} is locked by another consumer.")

    async def mark_as_completed(self, event_id: str) -> None:
        stmt = (
            update(consumer_processed_events_table)
            .where(consumer_processed_events_table.c.event_id == event_id)
            .values(status=ProcessingStatus.COMPLETED)
        )
        await self._session.execute(stmt)
        log.info(f"Marked event {event_id} as COMPLETED within transaction.")
