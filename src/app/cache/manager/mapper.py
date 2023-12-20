from loguru import logger

from app import settings
from app.cache.manager.managers import MemoryCacheManager, RedisCacheManager


CACHE_MANAGER_MAP = {
    'memory': MemoryCacheManager,
    'redis': RedisCacheManager,
    'default': RedisCacheManager,
}

cache_manager = CACHE_MANAGER_MAP.get(settings.CACHE)

if not cache_manager:
    cache_manager = CACHE_MANAGER_MAP.get('default')

logger.info(
    'Загружен менеджер кеша {cache}'.format(
        cache=cache_manager.name(),
    ),
)
