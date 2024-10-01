from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import check_cat_exist
from core.db import get_async_session
from crud.cat import cat_crud
from models import Cat
from schemas.cat import CatCreate, CatDB, CatUpdate

router = APIRouter(tags=['Котята'])


@router.post('/', response_model=CatDB,
             status_code=status.HTTP_201_CREATED)
async def create_cat(
        data_in: CatCreate,
        session: AsyncSession = Depends(get_async_session),
) -> Cat:
    """Добавление нового котёнка."""
    return await cat_crud.create(obj_in=data_in, session=session)


@router.get('/', response_model=list[CatDB])
async def get_cats(
        session: AsyncSession = Depends(get_async_session),
) -> list[Cat]:
    """Получение списка котят."""
    return await cat_crud.get_multi(session=session)


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
