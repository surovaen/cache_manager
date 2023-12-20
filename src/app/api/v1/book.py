from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response

from app.database import get_database
from app.db.repository import author_repo, book_repo
from app.models.author import Author
from app.models.book import Book
from app.models.response import BookAuthorsGetResponse, BookCommonResponse


router = APIRouter()


@router.get(
    path='/book',
    summary='Запрос книги и ее автора',
    status_code=status.HTTP_200_OK,
)
async def get_book_and_author(
        book_id: str = None,
        title: str = None,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """
    Эндпоинт получения книг и их авторов.

    book_id - Фильтрация по id книги;
    title - Фильтрация по наименованию книги.
    """
    response_model = BookCommonResponse(response=[])
    books = await book_repo.filter(
        conn=conn,
        book_id=book_id,
        title=title,
    )

    for book in books:
        author = await author_repo.filter(
            conn=conn,
            author_id=book.get('author_id'),
        )
        book_and_author = BookAuthorsGetResponse(
            **book,
            author=Author(**author[0]),
        )
        response_model.response.append(book_and_author)

    return JSONResponse(content=response_model.dict())


@router.put(
    '/book',
    summary='Обновление информации о книге',
    status_code=status.HTTP_200_OK,
)
async def update_book(
        book: Book,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт обновления информации о книге."""
    await book_repo.update(
        conn=conn,
        book=book,
    )

    return Response()


@router.delete(
    '/book',
    summary='Удаление книги',
    status_code=status.HTTP_200_OK,
)
async def delete_book(
        book_id: str = None,
        conn: AsyncIOMotorClient = Depends(get_database),
):
    """Эндпоинт удаления книги."""
    if not book_id:
        response = 'Не указан book_id'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response,
        )

    await book_repo.delete(
        conn=conn,
        book_id=book_id,
    )

    return Response()
