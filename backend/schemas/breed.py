from pydantic import BaseModel, Field

from core.constants import (
    EXAMPLE_BREED_DESCR,
    EXAMPLE_BREED_ID,
    EXAMPLE_BREED_NAME,
)


class BreedCreate(BaseModel):
    """Схема Pydantic-модели Breed для создания объекта в БД."""

    name: str = Field(example=EXAMPLE_BREED_NAME)
    description: str = Field(example=EXAMPLE_BREED_DESCR)

    class Config:
        extra = 'ignore'
        str_min_length = 1


class BreedUpdate(BreedCreate):
    """Схема Pydantic-модели Breed для изменения объекта в БД."""

    name: str | None = Field(default=None, example=EXAMPLE_BREED_NAME)
    description: str | None = Field(default=None, example=EXAMPLE_BREED_DESCR)


class BreedDB(BreedCreate):
    """Схема Pydantic-модели Breed для работы с БД."""

    id: int = Field(example=EXAMPLE_BREED_ID)

    class Config:
        from_attributes = True
