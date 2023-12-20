import abc
from typing import List, Optional

from app.core.cache_manager import BaseCacheManager
from app.core.repository import BaseRepository


class BaseCacheDecorator(abc.ABC):
    """Базовый класс декоратора выполнения кэш-операций."""

    def __init__(
            self,
            repository: BaseRepository,
            cache_manager: BaseCacheManager,
            related_repository: 'BaseCacheDecorator' = None,
    ):
        """Инициализация репозитория коллекции и менеджера кэша."""
        self._repository = repository
        self._cache_manager = cache_manager
        self._related_repository = related_repository

    @property
    def repo(self) -> BaseRepository:
        """Получение репозитория коллекции."""
        return self._repository

    @property
    def cache(self) -> BaseCacheManager:
        """Получение менеджера кэша."""
        return self._cache_manager

    @property
    def related_repo(self) -> 'BaseCacheDecorator':
        """Получение связанного класса-декоратора."""
        return self._related_repository

    async def set_cache(self, *args, **kwargs) -> None:
        """Метод записи в кеш."""
        await self.cache.set(*args, **kwargs)

    async def get_cache(self, *args, **kwargs) -> Optional[List[dict]]:
        """Метод получения записи из кэша."""
        return await self.cache.get(*args, **kwargs)

    async def delete_cache(self) -> None:
        """Метод удаления кэша."""
        await self.cache.delete()
