import abc
from typing import List, Optional

from app.core.singleton import Singleton


class BaseStorage(metaclass=Singleton):
    """Базовый класс хранилища кэша."""

    @abc.abstractmethod
    async def add(self, *args, **kwargs) -> None:
        """Метод добавления записи в кеш."""

    @abc.abstractmethod
    async def get(self, *args, **kwargs) -> Optional[List[dict]]:
        """Метод получения записи из кэша."""

    @abc.abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        """Метод удаления записи из кеша."""
