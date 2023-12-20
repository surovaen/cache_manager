from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings
from app.core.repository import BaseRepository
from app.models.author import Author, AuthorBase


class AuthorRepository(BaseRepository):
    """Репозиторий коллекции Автор в MongoDB."""

    db_name = settings.MONGO_DB
    collection = settings.COLLECTIONS['authors']

    async def create(
            self,
            conn: AsyncIOMotorClient,
            author: AuthorBase,
    ) -> ObjectId:
        """Метод создания записи в коллекции Автор."""
        created_author = await super()._create(conn, author.dict())
        return created_author.inserted_id

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            author_id: str = None,
            name: str = None,
    ) -> List[dict]:
        """Метод получения записей из коллекции Автор с учетом фильтров."""
        params = dict()

        if author_id:
            params.update(
                {
                    '_id': ObjectId(author_id),
                }
            )

        if name:
            params.update(
                {
                    'name': {
                        '$regex': name,
                        '$options': 'i',
                    }
                }
            )

        result = await super()._filter(conn, params)
        return [item async for item in result]

    async def delete(
            self,
            conn: AsyncIOMotorClient,
            author_id: str,
    ) -> None:
        """Метод удаления записи из коллекции Автор."""
        params = {'_id': ObjectId(author_id)}
        await super()._delete(conn, params)

    async def update(
            self,
            conn: AsyncIOMotorClient,
            author: Author,
    ) -> None:
        """Метод обновления записи из коллекции Автор."""
        updated_id = {'_id': ObjectId(author.id)}
        params = author.dict(exclude={'id'})
        await super()._update(conn, updated_id, params)
