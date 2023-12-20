from typing import Dict, List, Optional

from app.core.storage import BaseStorage


class MemoryStorage(BaseStorage):
    """Класс хранилища кэша в оперативной памяти."""

    _container = {}

    @property
    def container(self) -> Dict[str, List[dict]]:
        """Получение контейнера с данными кеша."""
        return self._container

    async def add(
            self,
            key: str,
            value: List[dict],
    ) -> None:
        """Метод добавления записи в кеш."""
        self.container[key] = value

    async def get(
            self,
            key: str,
    ) -> Optional[List[dict]]:
        """Метод получения записи из кэша."""
        return self.container.get(key)

    async def delete(
            self,
    ) -> None:
        """Метод удаления записей из кеша."""
        self.container.clear()
