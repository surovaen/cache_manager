from motor.motor_asyncio import AsyncIOMotorClient

from app.core.decorator import BaseCacheDecorator
from app.models.avatar import AvatarBase


class AvatarCacheDecorator(BaseCacheDecorator):
    """Класс-обертка над репозиторием коллекции Аватар для кэширования операций."""

    async def create(
            self,
            conn: AsyncIOMotorClient,
            avatar: AvatarBase,
    ):
        """Метод создания записи в коллекции Аватар."""
        return await self.repo.create(
            conn=conn,
            avatar=avatar,
        )

    async def filter(
            self,
            conn: AsyncIOMotorClient,
            avatar_id: str = None,
            author_id: str = None,
    ):
        """Метод получения записей из коллекции Аватар с учетом фильтров."""
        result = await self.get_cache(
            request=[
                avatar_id,
                author_id,
            ],
        )

        if result:
            return result

        result = await self.repo.filter(
            conn=conn,
            avatar_id=avatar_id,
            author_id=author_id,
        )

        await self.set_cache(
            request=[
                avatar_id,
                author_id,
            ],
            value=result,
        )

        return result
