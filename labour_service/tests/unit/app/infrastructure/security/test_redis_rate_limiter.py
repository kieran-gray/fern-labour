import logging
from unittest.mock import Mock

import pytest
from fakeredis import FakeValkey
from redis import RedisError

from src.core.infrastructure.security.rate_limiting.interface import RateLimiter
from src.core.infrastructure.security.rate_limiting.redis import RedisRateLimiter

MODULE = "src.core.infrastructure.security.rate_limiting.redis"


@pytest.fixture
def rate_limiter() -> RateLimiter:
    return RedisRateLimiter(FakeValkey())


def test_rate_limit_allowed(rate_limiter: RateLimiter) -> None:
    assert rate_limiter.is_allowed(key="test:key", limit=1, expiry=60)


def test_rate_limit_exceeded(rate_limiter: RateLimiter) -> None:
    assert not rate_limiter.is_allowed(key="test:key", limit=0, expiry=60)


def test_redis_error_returns_true(caplog: pytest.LogCaptureFixture):
    redis = Mock()
    redis.incr = Mock(side_effect=RedisError())
    rate_limiter = RedisRateLimiter(redis=redis)
    with caplog.at_level(logging.ERROR, MODULE):
        assert rate_limiter.is_allowed(key="test:key", limit=1, expiry=60)
        assert len(caplog.records) == 1
        assert "Redis error during rate limit check for key" in caplog.messages[0]


def test_exception_returns_true(caplog: pytest.LogCaptureFixture):
    redis = Mock()
    redis.incr = Mock(side_effect=Exception())
    rate_limiter = RedisRateLimiter(redis=redis)
    with caplog.at_level(logging.ERROR, MODULE):
        assert rate_limiter.is_allowed(key="test:key", limit=1, expiry=60)
        assert len(caplog.records) == 1
        assert "Unexpected error during rate limit check for key" in caplog.messages[0]
