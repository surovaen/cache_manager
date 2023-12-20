import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = '.env'
load_dotenv(dotenv_path)


class Config:
    """Настройки проекта."""

    DEBUG = os.environ.get('DEBUG', False)
    RELOAD = os.environ.get('RELOAD', False)

    APP_HOST = os.environ.get('APP_HOST', 'localhost')
    APP_PORT = int(os.environ.get('APP_PORT', '9000'))
    APP_WORKERS = int(os.environ.get('APP_WORKERS', '1'))
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*')

    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))
    MONGO_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'admin')
    MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'admin')
    MONGO_DB = os.environ.get('MONGO_INITDB_DATABASE', 'app')
    MONGODB_URL = 'mongodb://{user}:{password}@{host}:{port}/{db}?authSource=admin&retryWrites=true&w=majority'.format(
        user=MONGO_USER,
        password=MONGO_PASSWORD,
        host=MONGO_HOST,
        port=MONGO_PORT,
        db=MONGO_DB,
    )

    COLLECTIONS = {
        'authors': 'authors',
        'books': 'books',
        'avatars': 'avatars',
    }

    BASE_DIR = Path(__file__).resolve().parent
    MEDIA_DIR = Path(BASE_DIR / 'media')

    CACHE = os.environ.get('CACHE', 'default')

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'


if not Path(Config.MEDIA_DIR).exists():
    Path(Config.MEDIA_DIR).mkdir(exist_ok=True)
