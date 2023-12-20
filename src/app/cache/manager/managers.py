from app.cache.storage.memory import MemoryStorage
from app.cache.storage.redis import RedisStorage
from app.core.cache_manager import BaseCacheManager


class MemoryCacheManager(BaseCacheManager):
    """Менеджер кэша в оперативной памяти."""

    _name = 'Memory'
    _store = MemoryStorage


class RedisCacheManager(BaseCacheManager):
    """Менеджер кэша в Redis."""

    _name = 'Redis'
    _store = RedisStorage
