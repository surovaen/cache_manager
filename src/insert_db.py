import asyncio

from app.database import close_mongodb_connection, connect_to_mongodb, db
from app.db.author import AuthorRepository
from app.db.book import BookRepository
from app.models.author import AuthorBase
from app.models.book import BookBase


data = [
    {
        'name': 'Фёдор Михайлович Достоевский',
        'books': [
            {
                'title': 'Идиот',
            },
            {
                'title': 'Бесы',
            },
        ],
    },
    {
        'name': 'Нил Гейман',
        'books': [
            {
                'title': 'Песочный человек',
            },
            {
                'title': 'Американские боги',
            },
        ],
    },
    {
        'name': 'Лю Цысинь',
        'books': [
            {
                'title': 'Задача трёх тел',
            },
            {
                'title': 'Блуждающая земля',
            },
        ],
    },
]


async def insert_db():
    """Заполнение БД."""
    await connect_to_mongodb()

    conn = db.client
    for author in data:
        author_id = await AuthorRepository().create(
            conn=conn,
            author=AuthorBase(name=author.get('name')),
        )
        await BookRepository().bulk_create(
            conn=conn,
            books=[BookBase(title=book.get('title')) for book in author.get('books')],
            author_id=str(author_id)
        )

    await close_mongodb_connection()


if __name__ == '__main__':
    asyncio.run(insert_db())
