import logging
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from src.core.infrastructure.security.rate_limiting.in_memory import CacheEntry, InMemoryRateLimiter
from src.core.infrastructure.security.rate_limiting.interface import RateLimiter

MODULE = "src.core.infrastructure.security.rate_limiting.in_memory"


@pytest.fixture
def rate_limiter() -> RateLimiter:
    return InMemoryRateLimiter()


def test_rate_limit_allowed(rate_limiter: RateLimiter) -> None:
    assert rate_limiter.is_allowed(key="test:key", limit=1, expiry=60)


def test_rate_limit_exceeded(rate_limiter: RateLimiter) -> None:
    assert not rate_limiter.is_allowed(key="test:key", limit=0, expiry=60)


def test_rate_limit_multiple_keys(rate_limiter: RateLimiter) -> None:
    assert rate_limiter.is_allowed(key="test:1", limit=1, expiry=60)
    assert not rate_limiter.is_allowed(key="test:1", limit=1, expiry=60)
    assert rate_limiter.is_allowed(key="test:2", limit=1, expiry=60)
    assert not rate_limiter.is_allowed(key="test:2", limit=1, expiry=60)


def test_rate_limit_entry_expired(rate_limiter: RateLimiter) -> None:
    key = "test:key"
    expiry_seconds = 60
    expiry = datetime.now() - timedelta(seconds=expiry_seconds)
    rate_limiter._data = {key: CacheEntry(key=key, count=10, expiry_seconds=1000, expiry=expiry)}
    assert rate_limiter.is_allowed(key, limit=1, expiry=expiry_seconds)
    assert not rate_limiter.is_allowed(key, limit=1, expiry=expiry_seconds)


def test_exception_returns_true(caplog: pytest.LogCaptureFixture):
    rate_limiter = InMemoryRateLimiter()
    rate_limiter._incr = Mock(side_effect=Exception())
    with caplog.at_level(logging.ERROR, MODULE):
        assert rate_limiter.is_allowed(key="test:key", limit=1, expiry=60)
        assert len(caplog.records) == 1
        assert "Unexpected error during rate limit check for key" in caplog.messages[0]
