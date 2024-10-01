from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import check_breed_exist, check_breed_name_duplicate
from core.db import get_async_session
from crud.breed import breed_crud
from models import Breed
from schemas.breed import BreedCreate, BreedDB, BreedUpdate

router = APIRouter(tags=['Породы'])


@router.post('/', response_model=BreedDB,
             status_code=status.HTTP_201_CREATED)
async def create_breed(
        data_in: BreedCreate,
        session: AsyncSession = Depends(get_async_session),
) -> Breed:
    """Добавление новой породы."""
    await check_breed_name_duplicate(breed_name=data_in.name, session=session)
    return await breed_crud.create(obj_in=data_in, session=session)


@router.get('/', response_model=list[BreedDB])
async def get_breeds(
        session: AsyncSession = Depends(get_async_session),
) -> list[Breed]:
    """Получение списка пород."""
    return await breed_crud.get_multi(session=session)


@router.get('/{id}/', response_model=BreedDB)
async def get_breed(
        id: int, session: AsyncSession = Depends(get_async_session),
) -> Breed:
    """Получение определенной породы."""
    return await check_breed_exist(breed_id=id, session=session)


@router.patch('/{id}/', response_model=BreedDB,
              status_code=status.HTTP_201_CREATED)
async def update_breed(
        id: int, data_in: BreedUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> Breed:
    """Обновление определенной породы."""
    breed_to_upd = await check_breed_exist(breed_id=id, session=session)
    if data_in.name and data_in.name != breed_to_upd.name:
        await check_breed_name_duplicate(
            breed_name=data_in.name, session=session
        )
    return await breed_crud.update(
        db_obj=breed_to_upd, obj_in=data_in, session=session
    )


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_breed(
        id: int, session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удаление породы."""
    breed_to_del = await check_breed_exist(breed_id=id, session=session)
    await breed_crud.remove(breed_to_del, session)
