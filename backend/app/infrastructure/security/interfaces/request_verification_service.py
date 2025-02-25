from typing import Protocol


class RequestVerificationService(Protocol):
    """Protocol for request verification by token."""

    async def verify(self, token: str, ip: str) -> bool:
        """
        Verify the given token and return bool indicating success or failure.
        """
