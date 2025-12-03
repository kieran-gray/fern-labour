from typing import Protocol


class RateLimiter(Protocol):
    """Protocol for rate limiting requests."""

    def is_allowed(self, key: str, limit: int, expiry: int) -> bool:
        """Checks if the action associated with the key is allowed under the limit."""
