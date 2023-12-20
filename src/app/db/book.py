from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings
from app.core.repository import BaseRepository
from app.models.book import Book, BookBase, BookCreate


class BookRepository(BaseRepository):
    """Репозиторий коллекции Книга в MongoDB."""

    db_name = settings.MONGO_DB
    collection = settings.COLLECTIONS['books']

    async def create(
            self,
            conn: AsyncIOMotorClient,
            book: BookBase,
            author_id: str,
    ) -> ObjectId:
        """Метод создания записи в коллекции Книга."""
        book_data = BookCreate(author_id=author_id, **book.dict())
        result = await super()._create(conn, book_data.dict())
        return result.inserted_id

    async def bulk_create(
            self,
            conn: AsyncIOMotorClient,
            books: List[BookBase],
            author_id: str,
    ) -> List[ObjectId]:
        """Метод создания нескольких записей в коллекции Книга."""
        books = [BookCreate(**book.dict(), author_id=author_id).dict() for book in books]
        result = await super()._bulk_create(conn, books)
        return result.inserted_ids

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            book_id: str = None,
            author_id: str = None,
            title: str = None,
    ) -> List[dict]:
        """Метод получения записей из коллекции Книга с учетом фильтров."""
        params = dict()

        if book_id:
            params.update(
                {
                    '_id': ObjectId(book_id),
                }
            )

        if author_id:
            params.update(
                {
                    'author_id': author_id,
                }
            )

        if title:
            params.update(
                {
                    'title': {
                        '$regex': title,
                        '$options': 'i',
                    }
                }
            )
        result = await super()._filter(conn, params)
        return [item async for item in result]

    async def delete(
            self,
            conn: AsyncIOMotorClient,
            book_id: str = None,
            author_id: str = None,
    ) -> None:
        """Метод удаления записи из коллекции Автор."""
        params = dict()

        if book_id:
            params.update(
                {
                    '_id': ObjectId(book_id),
                },
            )

        if author_id:
            params.update(
                {
                    'author_id': author_id,
                },
            )

        return await super()._delete(conn, params)

    async def update(
            self,
            conn: AsyncIOMotorClient,
            book: Book,
    ) -> None:
        """Метод обновления записи из коллекции Книга."""
        updated_id = {'_id': ObjectId(book.id)}
        params = book.dict(exclude={'id'})
        await super()._update(conn, updated_id, params)
