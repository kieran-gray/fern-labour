from typing import Protocol


class RequestVerificationService(Protocol):
    """Protocol for request verification by token."""

    async def verify(self, token: str, ip: str) -> None:
        """
        Verify the given token and raise exception if not valid.
        """
