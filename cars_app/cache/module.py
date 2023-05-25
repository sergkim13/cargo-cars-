import json

from aioredis.client import Redis
from fastapi.encoders import jsonable_encoder

from cars_app.cache.abstract_cache import AbstractCache
from cars_app.cache.settings import EXPIRE_TIME, redis_client


class RedisCache(AbstractCache):
    """Cache with Redis client."""

    def __init__(self, cache_client: Redis) -> None:
        """Init instance with given client."""
        self.redis_client = cache_client

    async def get(self, key: str):
        """Gets cached value."""
        value = await self.redis_client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: str, expire_time=EXPIRE_TIME):
        """Set value to cache."""
        value = json.dumps(jsonable_encoder(value))
        await self.redis_client.set(key, value, expire_time)

    async def clear(self, key: str):
        """Clear value or values frim cache."""
        if key == 'all':
            async for key in self.redis_client.scan_iter('cargo-*'):
                await self.redis_client.delete(key)
        else:
            await self.redis_client.delete(key)


def get_redis_cache():
    """Returns `RedisCache` instance for dependency injection."""
    return RedisCache(cache_client=redis_client)
