import abc

from motor.motor_asyncio import AsyncIOMotorClient


class BaseRepository(abc.ABC):
    """Абстрактный класс репозитория MongoDB."""

    db_name: str = None
    collection: str = None

    async def _create(
            self,
            conn: AsyncIOMotorClient,
            *args,
            **kwargs,
    ):
        """Метод создания одной записи в MongoDB."""
        return await conn[self.db_name][self.collection].insert_one(*args, **kwargs)

    async def _bulk_create(
            self,
            conn: AsyncIOMotorClient,
            *args,
            **kwargs,
    ):
        """Метод создания нескольких записей в MongoDB."""
        return await conn[self.db_name][self.collection].insert_many(*args, **kwargs)

    async def _filter(
            self,
            conn: AsyncIOMotorClient,
            *args,
            **kwargs,
    ):
        """Метод получения записей с учетом фильтра в MongoDB."""
        return conn[self.db_name][self.collection].find(*args, **kwargs)

    async def _delete(
            self,
            conn: AsyncIOMotorClient,
            *args,
            **kwargs,
    ):
        """Метод удаления одной записи в MongoDB."""
        return await conn[self.db_name][self.collection].delete_one(*args, **kwargs)

    async def _update(
            self,
            conn: AsyncIOMotorClient,
            *args,
            **kwargs,
    ):
        """Метод обновления одной записи в MongoDB."""
        return await conn[self.db_name][self.collection].replace_one(*args, **kwargs)

    async def create(self, *args, **kwargs):
        """Публичный метод создания одной записи в MongoDB."""
        pass

    async def bulk_create(self, *args, **kwargs):
        """Публичный метод создания нескольких записей в MongoDB."""
        pass

    async def filter(self, *args, **kwargs):
        """Публичный метод получения записей с учетом фильтра в MongoDB."""
        pass

    async def delete(self, *args, **kwargs):
        """Публичный метод удаления одной записи в MongoDB."""
        pass

    async def update(self, *args, **kwargs):
        """Публичный метод обновления одной записи в MongoDB."""
        pass
