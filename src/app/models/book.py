from pydantic import BaseModel

from app.models.mixins import IDModelMixin


class BookBase(BaseModel):
    """Модель Книга базовая."""

    title: str


class BookCreate(BookBase):
    """Модель Книга для создания записи в коллекции."""
    author_id: str


class Book(BookCreate, IDModelMixin):
    """Модель Книга."""
