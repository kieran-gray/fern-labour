import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.core.infrastructure.security.rate_limiting.interface import RateLimiter

log = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    key: str
    count: int
    expiry: datetime

    def __init__(
        self, key: str, count: int, expiry_seconds: int, expiry: datetime | None = None
    ) -> None:
        self.key = key
        self.count = count
        self.expiry = expiry or self.get_expiry(expiry_seconds)

    def get_expiry(self, expiry_seconds: int) -> datetime:
        return datetime.now() + timedelta(seconds=expiry_seconds)

    def set_expiry(self, expiry_seconds: int) -> None:
        self.expiry = self.get_expiry(expiry_seconds)

    def increment(self) -> None:
        self.count += 1


class InMemoryRateLimiter(RateLimiter):
    def __init__(self) -> None:
        self._data: dict[str, CacheEntry] = {}

    def _incr(self, key: str, expiry_seconds: int) -> int:
        entry = self._data.get(key)
        if not entry:
            entry = CacheEntry(key=key, count=0, expiry_seconds=expiry_seconds)
            entry.set_expiry(expiry_seconds)
            self._data[entry.key] = entry
            log.debug(f"Key '{key}' created.")
        if entry.expiry < datetime.now():
            entry.set_expiry(expiry_seconds)
            entry.count = 0
        entry.increment()
        return entry.count

    def is_allowed(self, key: str, limit: int, expiry: int) -> bool:
        log.debug(f"Running rate-limit check for {key=}")
        try:
            current_count = self._incr(key, expiry)
            log.debug(f"Current count for {key} = {current_count}")
            if current_count > limit:
                log.warning(f"Rate limit exceeded for key '{key}'")
                return False
            return True
        except Exception as e:
            log.error(f"Unexpected error during rate limit check for key '{key}': {e}")
            return True
