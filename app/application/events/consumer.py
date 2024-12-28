from typing import Protocol


class EventConsumer(Protocol):
    """Protocol for event consumers"""

    async def start(self) -> None:
        """Start consuming events"""

    async def stop(self) -> None:
        """Stop consuming events"""

    async def is_healthy(self) -> bool:
        """Check if the consumer is healthy and connected"""
