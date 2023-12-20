from typing import List

from pydantic import BaseModel

from app.models.author import AuthorBase
from app.models.book import BookBase


class AuthorBooksPostRequest(BaseModel):
    """Модель POST запроса на создание автора и его книг."""

    author: AuthorBase
    books: List[BookBase]
