import aioredis
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings


class DataBase:
    """Класс инициализации клиента БД MongoDB."""

    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    """Получение клиента MongoDB."""
    return db.client


async def connect_to_mongodb():
    """Подключение к MongoDB."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    logger.info('Подключение к MongoDB.')


async def close_mongodb_connection():
    """Закрытие подключения к MongoDB."""
    db.client.close()
    logger.info('Закрытие подключения к MongoDB.')


redis = aioredis.from_url(
    settings.REDIS_URL,
    encoding='utf-8',
    decode_responses=True,
)
