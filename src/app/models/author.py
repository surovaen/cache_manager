from pydantic import BaseModel

from app.models.mixins import IDModelMixin


class AuthorBase(BaseModel):
    """Модель Автор базовая."""

    name: str


class Author(AuthorBase, IDModelMixin):
    """Модель Автор."""
