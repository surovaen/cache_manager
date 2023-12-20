import abc
from typing import List, Optional

from app.core.helpers import process_object_id
from app.core.storage import BaseStorage


class BaseCacheManager(abc.ABC):
    """Базовый класс менеджера кэша."""

    _name = None
    _store = None
    _template = '{repo}_{params}'

    def __init__(self, repo: str):
        """Инициализация хранилища кэша для репозитория коллекции."""
        self._repo = repo
        self._store = self._store()

    @classmethod
    def name(cls) -> str:
        """Наименование менеджера."""
        return cls._name

    @property
    def store(self) -> BaseStorage:
        """Получение хранилища кэша."""
        return self._store

    def key_template(
            self,
            request: List[Optional[str]],
    ):
        """Формирование ключа."""
        params = [key for key in request if key]

        if params:
            return self._template.format(
                repo=self._repo,
                params='_'.join(params),
            )
        return self._template.format(
            repo=self._repo,
            params='all',
        )

    async def set(
            self,
            request: List[str],
            value: List[dict],
    ) -> None:
        """Добавление записи в кеш."""
        key = self.key_template(request)
        value = process_object_id(value)
        await self.store.add(key, value)

    async def get(
            self,
            request: List[str],
    ) -> Optional[List[dict]]:
        """Получение записи из кеша."""
        key = self.key_template(request)
        return await self.store.get(key)

    async def delete(
            self,
    ) -> None:
        """Удаление записи из кеша."""
        await self.store.delete()
