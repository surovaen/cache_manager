from pydantic import BaseModel

from app.models.mixins import IDModelMixin


class AvatarBase(BaseModel):
    """Модель Аватара базовая."""

    image: str
    author_id: str


class Avatar(AvatarBase, IDModelMixin):
    """Модель аватара Автора."""
