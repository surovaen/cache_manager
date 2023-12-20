import json
from typing import List, Optional

from app.core.storage import BaseStorage
from app.database import redis


class RedisStorage(BaseStorage):
    """Класс хранилища кэша в Redis."""

    async def add(
            self,
            key: str,
            value: List[dict],
    ) -> None:
        """Метод добавления записи в кеш."""
        await redis.set(
            name=key,
            value=json.dumps(value),
        )

    async def get(
            self,
            key: str,
    ) -> Optional[List[dict]]:
        """Метод получения записи из кэша."""
        result = await redis.get(key)
        return json.loads(result) if result else None

    async def delete(
            self,
    ) -> None:
        """Метод удаления записи из кеша."""
        await redis.flushall(asynchronous=True)
