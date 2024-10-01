from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.pagination import get_next_and_previous_urls
from api.validators import check_breed_exist, check_breed_name_duplicate
from core.constants import (
    BREED_API_URL,
    BREED_SEARCH_DESCR,
    PAGE_NUMBER_DESCR,
    QUERY_LIMIT,
    QUERY_LIMIT_DESCR,
    QUERY_PAGE,
)
from core.db import get_async_session
from crud.breed import breed_crud
from models import Breed
from schemas.breed import BreedCreate, BreedDB, BreedList, BreedUpdate

router = APIRouter(tags=['Породы'])


@router.post('/', response_model=BreedDB, status_code=status.HTTP_201_CREATED)
async def create_breed(
    data_in: BreedCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Breed:
    """Добавление новой породы."""
    await check_breed_name_duplicate(breed_name=data_in.name, session=session)
    return await breed_crud.create(obj_in=data_in, session=session)


@router.get('/', response_model=BreedList)
async def get_breeds(
    session: AsyncSession = Depends(get_async_session),
    search: str | None = Query(default=None, description=BREED_SEARCH_DESCR),
    limit: int = Query(
        gt=0, default=QUERY_LIMIT, description=QUERY_LIMIT_DESCR
    ),
    page: int = Query(gt=0, default=QUERY_PAGE, description=PAGE_NUMBER_DESCR),
) -> dict[str, int | str | list]:
    """Получение списка пород."""
    breeds_list, total_count = await breed_crud.get_breeds_list(
        session, search, limit, page
    )
    next_url, prev_url = get_next_and_previous_urls(
        BREED_API_URL, total_count, limit, page, search=search
    )

    return {
        'count': total_count,
        'next': next_url,
        'previous': prev_url,
        'results': breeds_list,
    }


@router.get('/{id}/', response_model=BreedDB)
async def get_breed(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Breed:
    """Получение определенной породы."""
    return await check_breed_exist(breed_id=id, session=session)


@router.patch(
    '/{id}/', response_model=BreedDB, status_code=status.HTTP_201_CREATED
)
async def update_breed(
    id: int,
    data_in: BreedUpdate,
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
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удаление породы."""
    breed_to_del = await check_breed_exist(breed_id=id, session=session)
    await breed_crud.remove(breed_to_del, session)
