from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.decorator import BaseCacheDecorator
from app.models.author import Author, AuthorBase


class AuthorCacheDecorator(BaseCacheDecorator):
    """Класс-обертка над репозиторием коллекции Автор для кэширования операций."""

    async def create(
            self,
            conn: AsyncIOMotorClient,
            author: AuthorBase,
    ) -> ObjectId:
        """Метод создания записи в коллекции Автор."""
        author_id = await self.repo.create(
            conn=conn,
            author=author,
        )
        await self.delete_cache()
        return author_id

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            author_id: str = None,
            name: str = None,
    ) -> List[dict]:
        """Метод получения записей из коллекции Автор с учетом фильтров."""
        result = await self.get_cache(
            request=[
                author_id,
                name,
            ],
        )

        if result:
            return result

        result = await self.repo.filter(
            conn=conn,
            author_id=author_id,
            name=name,
        )

        await self.set_cache(
            request=[
                author_id,
                name,
            ],
            value=result,
        )

        return result

    async def delete(
            self,
            conn: AsyncIOMotorClient,
            author_id: str,
    ) -> None:
        """Метод удаления записи из коллекции Автор."""
        await self.repo.delete(
            conn=conn,
            author_id=author_id,
        )
        await self.delete_cache()

    async def update(
            self,
            conn: AsyncIOMotorClient,
            author: Author,
    ) -> None:
        """Метод обновления записи из коллекции Автор."""
        await self.repo.update(
            conn=conn,
            author=author,
        )
        await self.delete_cache()
