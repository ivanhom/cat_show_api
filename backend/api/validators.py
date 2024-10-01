from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    ERROR_BREED_EXISTS,
    ERROR_BREED_DOESNT_EXIST,
)
from crud.breed import breed_crud
from models import Breed


async def check_breed_name_duplicate(
        breed_name: str, session: AsyncSession
) -> None:
    """Проверка на уникальность вводимого имени породы."""
    breed = await breed_crud.get_by_attribute(
        attr_name='name', attr_value=breed_name, session=session
    )
    if breed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_BREED_EXISTS
        )


async def check_breed_exist(breed_id: int, session: AsyncSession) -> Breed:
    """Проверяет, что порода уже есть в БД и возвращает её."""
    breed = await breed_crud.get_by_attribute(
        attr_name='id', attr_value=breed_id, session=session
    )
    if not breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_BREED_DOESNT_EXIST
        )
    return breed
