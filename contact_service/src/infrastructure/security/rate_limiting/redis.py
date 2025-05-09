import logging

from redis import Redis, RedisError

from src.infrastructure.security.rate_limiting.interface import RateLimiter

log = logging.getLogger(__name__)


class RedisRateLimiter(RateLimiter):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def is_allowed(self, key: str, limit: int, expiry: int) -> bool:
        log.debug(f"Running rate-limit check for {key=}, {limit=}, {expiry=}")
        try:
            current_count = self._redis.incr(key)
            if current_count == 1:
                self._redis.expire(name=key, time=expiry)
                log.debug(f"Key '{key}' created.")
            log.debug(f"Current count for {key} = {current_count}")
            if current_count > limit:  # type: ignore
                log.warning(f"Rate limit exceeded for key '{key}'")
                return False
            return True
        except RedisError as e:
            log.error(f"Redis error during rate limit check for key '{key}': {e}")
            return True
        except Exception as e:
            log.error(f"Unexpected error during rate limit check for key '{key}': {e}")
            return True
