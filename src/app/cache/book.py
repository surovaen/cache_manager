from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.decorator import BaseCacheDecorator
from app.models.book import Book, BookBase


class BookCacheDecorator(BaseCacheDecorator):
    """Класс-обертка над репозиторием коллекции Книга для кэширования операций."""

    async def create(
            self,
            conn: AsyncIOMotorClient,
            book: BookBase,
            author_id: str,
    ):
        """Метод создания записи в коллекции Книга."""
        book_id = await self.repo.create(
            conn=conn,
            book=book,
            author_id=author_id,
        )
        await self.delete_cache()
        return book_id

    async def bulk_create(
            self,
            conn: AsyncIOMotorClient,
            books: List[BookBase],
            author_id: str,
    ):
        """Метод создания нескольких записей в коллекции Книга."""
        book_ids = await self.repo.bulk_create(
            conn=conn,
            books=books,
            author_id=author_id,
        )
        await self.delete_cache()
        return book_ids

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            book_id: str = None,
            author_id: str = None,
            title: str = None,
    ):
        """Метод получения записей из коллекции Книга с учетом фильтров."""
        result = await self.get_cache(
            request=[
                book_id,
                author_id,
                title,
            ],
        )

        if result:
            return result

        result = await self.repo.filter(
            conn=conn,
            book_id=book_id,
            author_id=author_id,
            title=title,
        )

        await self.set_cache(
            request=[
                book_id,
                author_id,
                title,
            ],
            value=result,
        )

        return result

    async def delete(
            self,
            conn: AsyncIOMotorClient,
            book_id: str = None,
            author_id: str = None,
    ):
        """Метод удаления записи из коллекции Автор."""
        await self.repo.delete(
            conn=conn,
            book_id=book_id,
            author_id=author_id,
        )
        await self.delete_cache()

    async def update(
            self,
            conn: AsyncIOMotorClient,
            book: Book,
    ) -> None:
        """Метод обновления записи из коллекции Книга."""
        await self.repo.update(
            conn=conn,
            book=book,
        )
        await self.delete_cache()

    async def delete_cache(self) -> None:
        """Переопределение метода удаления кэша с учетом кэша связанного репозитория."""
        await super().delete_cache()
        await self.related_repo.delete_cache()
