from pydantic import BaseModel, Field

from core.constants import (
    EXAMPLE_BREED_COUNT,
    EXAMPLE_BREED_DESCR,
    EXAMPLE_BREED_ID,
    EXAMPLE_BREED_NAME,
    EXAMPLE_BREED_NEXT_URL,
    EXAMPLE_BREED_PREV_URL,
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


class BreedList(BaseModel):
    """Схема для отображения модели Breed с пагинацией."""

    count: int = Field(example=EXAMPLE_BREED_COUNT)
    next: str | None = Field(example=EXAMPLE_BREED_NEXT_URL)
    previous: str | None = Field(example=EXAMPLE_BREED_PREV_URL)
    results: list[BreedDB]
