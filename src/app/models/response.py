from typing import List

from pydantic import BaseModel

from app.models.author import Author
from app.models.book import Book


class BookAuthorsGetResponse(Book):
    """Модель респонса информации о книге и авторе."""

    author: Author


class AuthorBooksGetResponse(Author):
    """Модель респонса информации об авторе и его книгах."""

    books: List[Book]


class AuthorCommonResponse(BaseModel):
    """Модель респонса информации об авторах и их книгах."""

    response: List[AuthorBooksGetResponse]


class BookCommonResponse(BaseModel):
    """Модель респонса о книгах и их авторах."""

    response: List[BookAuthorsGetResponse]
