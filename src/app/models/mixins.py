from pydantic import BaseModel, Field

from app.core.models import OID


class IDModelMixin(BaseModel):
    """Миксин, добавляющий id объекта модели."""

    id: OID = Field(alias='_id')

    class Config:
        allow_population_by_alias = True
