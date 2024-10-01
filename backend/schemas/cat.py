from pydantic import BaseModel, Field

from core.constants import (
    CAT_MAX_AGE,
    CAT_MIN_AGE,
    EXAMPLE_BREED_ID,
    EXAMPLE_CAT_AGE,
    EXAMPLE_CAT_COLOR,
    EXAMPLE_CAT_COUNT,
    EXAMPLE_CAT_DESCR,
    EXAMPLE_CAT_NAME,
    EXAMPLE_CAT_NEXT_URL,
    EXAMPLE_CAT_PREV_URL,
    EXAMPLE_CAT_SEX,
)

from core.enums import CatColor, CatSex
from schemas.breed import BreedDB


class CatCreate(BaseModel):
    """Схема Pydantic-модели Cat для создания объекта в БД."""

    name: str = Field(example=EXAMPLE_CAT_NAME)
    description: str = Field(example=EXAMPLE_CAT_DESCR)
    sex: CatSex = Field(example=EXAMPLE_CAT_SEX)
    months: int = Field(
        example=EXAMPLE_CAT_AGE, ge=CAT_MIN_AGE, le=CAT_MAX_AGE
    )
    color: CatColor = Field(example=EXAMPLE_CAT_COLOR)
    breed_id: int = Field(example=EXAMPLE_BREED_ID)

    class Config:
        extra = 'ignore'
        str_min_length = 1


class CatUpdate(CatCreate):
    """Схема Pydantic-модели Cat для изменения объекта в БД."""

    name: str | None = Field(default=None, example=EXAMPLE_CAT_NAME)
    description: str | None = Field(default=None, example=EXAMPLE_CAT_DESCR)
    sex: CatSex | None = Field(default=None, example=EXAMPLE_CAT_SEX)
    months: int | None = Field(
        default=None, example=EXAMPLE_CAT_AGE, ge=CAT_MIN_AGE, le=CAT_MAX_AGE
    )
    color: CatColor | None = Field(default=None, example=EXAMPLE_CAT_COLOR)
    breed_id: int | None = Field(default=None, example=EXAMPLE_BREED_ID)


class CatDB(CatCreate):
    """Схема Pydantic-модели Cat для работы с БД."""

    id: int
    breed: BreedDB | None
    breed_id: int | None = Field(exclude=True)

    class Config:
        from_attributes = True


class CatList(BaseModel):
    """Схема для отображения модели Cat с пагинацией."""

    count: int = Field(example=EXAMPLE_CAT_COUNT)
    next: str | None = Field(example=EXAMPLE_CAT_NEXT_URL)
    previous: str | None = Field(example=EXAMPLE_CAT_PREV_URL)
    results: list[CatDB]
