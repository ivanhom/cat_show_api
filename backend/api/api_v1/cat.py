from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.pagination import get_next_and_previous_urls
from api.validators import check_cat_exist
from core.constants import (
    CAT_BREED_SEARCH_DESCR,
    CAT_SEARCH_DESCR,
    CAT_API_URL,
    PAGE_NUMBER_DESCR,
    QUERY_LIMIT,
    QUERY_LIMIT_DESCR,
    QUERY_PAGE,
)
from core.db import get_async_session
from core.enums import CatColor, CatSex
from crud.cat import cat_crud
from models import Cat
from schemas.cat import CatCreate, CatDB, CatList, CatUpdate

router = APIRouter(tags=['Котята'])


@router.post('/', response_model=CatDB,
             status_code=status.HTTP_201_CREATED)
async def create_cat(
        data_in: CatCreate,
        session: AsyncSession = Depends(get_async_session),
) -> Cat:
    """Добавление нового котёнка."""
    return await cat_crud.create(obj_in=data_in, session=session)


@router.get('/', response_model=CatList)
async def get_cats(
        session: AsyncSession = Depends(get_async_session),
        search: str | None = Query(
            default=None, description=CAT_SEARCH_DESCR
        ),
        breed_id: int | None = Query(
            ge=0, default=None, description=CAT_BREED_SEARCH_DESCR
        ),
        sex: list[CatSex] = Query(default=[], description='USER_ROLE_DESCR'),
        color: list[CatColor] = Query(default=[], description='USER_ROLE_DESCR'),
        limit: int = Query(
            gt=0, default=QUERY_LIMIT, description=QUERY_LIMIT_DESCR
        ),
        page: int = Query(
            gt=0, default=QUERY_PAGE, description=PAGE_NUMBER_DESCR
        ),
) -> dict[str, int | str | list]:
    """Получение списка котят."""
    cats_list, total_count = await cat_crud.get_cats_list(
        session, search, breed_id, sex, color, limit, page
    )
    next_url, prev_url = get_next_and_previous_urls(
        CAT_API_URL,
        total_count,
        limit, page,
        search=search,
        breed_id=breed_id,
        sex=sex,
        color=color,
    )

    return {
        'count': total_count,
        'next': next_url,
        'previous': prev_url,
        'results': cats_list,
    }


@router.get('/{id}/', response_model=CatDB)
async def get_cat(
        id: int, session: AsyncSession = Depends(get_async_session),
) -> Cat:
    """Получение определенного котёнка."""
    return await check_cat_exist(cat_id=id, session=session)


@router.patch('/{id}/', response_model=CatDB,
              status_code=status.HTTP_201_CREATED)
async def update_cat(
        id: int, data_in: CatUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> Cat:
    """Обновление определенного котёнка."""
    cat_to_upd = await check_cat_exist(cat_id=id, session=session)
    return await cat_crud.update(
        db_obj=cat_to_upd, obj_in=data_in, session=session
    )


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(
        id: int, session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удаление котёнка."""
    cat_to_del = await check_cat_exist(cat_id=id, session=session)
    await cat_crud.remove(cat_to_del, session)
