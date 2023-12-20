from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from starlette.responses import JSONResponse, Response

from app.database import get_database
from app.db.repository import author_repo, book_repo
from app.models.author import Author
from app.models.book import Book
from app.models.request import AuthorBooksPostRequest
from app.models.response import AuthorBooksGetResponse, AuthorCommonResponse


router = APIRouter()


@router.get(
    path='/author',
    summary='Запрос авторов и их книг',
    status_code=status.HTTP_200_OK,
)
async def get_authors_and_books(
        author_id: str = None,
        name: str = None,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """
    Эндпоинт получения авторов и их книг.

    author_id - Фильтрация по id автора.
    name - Фильтрация по имени автора.
    """
    authors = await author_repo.filter(
        conn=conn,
        author_id=author_id,
        name=name,
    )
    response_model = AuthorCommonResponse(response=[])

    for author in authors:
        books = await book_repo.filter(
            conn=conn,
            author_id=str(author.get('_id')),
        )
        author_and_books = AuthorBooksGetResponse(
            **author,
            books=[Book(**book) for book in books],
        )
        response_model.response.append(author_and_books)

    return JSONResponse(content=response_model.dict())


@router.post(
    '/author',
    summary='Создание автора и его книг',
)
async def post_author_and_books(
        request: AuthorBooksPostRequest,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт создания автора и его книг."""
    author_id = await author_repo.create(
        conn=conn,
        author=request.author,
    )
    book_ids = await book_repo.bulk_create(
        conn=conn,
        books=request.books,
        author_id=str(author_id),
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'id': str(author_id),
            'book_ids': [str(book_id) for book_id in book_ids],
        },
    )


@router.put(
    '/author',
    summary='Обновление информации об авторе',
    status_code=status.HTTP_200_OK,
)
async def update_author(
        author: Author,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт обновления информации об авторе."""
    await author_repo.update(
        conn=conn,
        author=author,
    )

    return Response()


@router.delete(
    '/author',
    summary='Удаление автора и его книг',
    status_code=status.HTTP_200_OK,
)
async def delete_author_and_books(
        author_id: str,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт удаления автора и его книг."""
    await author_repo.delete(
        conn=conn,
        author_id=author_id,
    )
    await book_repo.delete(
        conn=conn,
        author_id=author_id,
    )

    return Response()
