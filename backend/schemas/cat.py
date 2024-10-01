from pydantic import BaseModel


class CatCreate(BaseModel):
    """Схема Pydantic-модели Cat для создания объекта в БД."""

    name: str

    class Config:
        extra = 'ignore'


class CatUpdate(CatCreate):
    """Схема Pydantic-модели Cat для изменения объекта в БД."""

    pass


class CatDB(CatCreate):
    """Схема Pydantic-модели Cat для работы с БД."""

    id: int

    class Config:
        from_attributes = True
