from abc import ABC, abstractmethod


class EventConsumer(ABC):
    """Abstract base class for event consumers"""

    @abstractmethod
    async def start(self) -> None:
        """Start consuming events"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop consuming events"""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if the consumer is healthy and connected"""
        pass
