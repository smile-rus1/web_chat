from typing import Any, Optional

from redis.asyncio import Redis

from src.interfaces.infrastructure.redis_db import IRedisDB


class RedisDB(IRedisDB):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        return await self._redis.set(key, value=value, ex=expire)

    async def get(self, key: str) -> Any:
        return await self._redis.get(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._redis.exists(key))
