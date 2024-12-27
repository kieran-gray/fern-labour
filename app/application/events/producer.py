from abc import ABC, abstractmethod

from app.domain.base.event import DomainEvent


class EventProducer(ABC):
    """Abstract base class for event producers"""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish single event."""

    @abstractmethod
    async def publish_batch(self, events: list[DomainEvent]) -> None:
        """Publish batch of events."""
