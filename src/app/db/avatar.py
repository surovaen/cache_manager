from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings
from app.core.repository import BaseRepository
from app.models.avatar import AvatarBase


class AvatarRepository(BaseRepository):
    """Репозиторий коллекции Аватар в MongoDB."""

    db_name = settings.MONGO_DB
    collection = settings.COLLECTIONS['avatars']

    async def create(
            self,
            conn: AsyncIOMotorClient,
            avatar: AvatarBase,
    ):
        """Метод создания записи в коллекции Аватар."""
        created_avatar = await super()._create(conn, avatar.dict())
        return created_avatar.inserted_id

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            avatar_id: str = None,
            author_id: str = None,
    ):
        """Метод получения записей из коллекции Аватар с учетом фильтров."""
        params = dict()

        if avatar_id:
            params.update(
                {
                    '_id': ObjectId(avatar_id),
                }
            )
        if author_id:
            params.update(
                {
                    'author_id': author_id,
                }
            )

        result = await super()._filter(conn, params)
        return [item async for item in result]
