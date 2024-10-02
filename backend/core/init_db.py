import contextlib
import csv
import logging

from core.db import get_async_session
from crud.breed import breed_crud
from crud.cat import cat_crud
from schemas.breed import BreedCreate
from schemas.cat import CatCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def fill_empty_db() -> None:
    """Вызов функции наполненияя БД заготовленными данными."""

    is_empty = await check_db_is_empty()

    if not is_empty:
        new_breeds = read_csv('start_data/breeds_data.csv', BreedCreate)
        new_cats = read_csv('start_data/cats_data.csv', CatCreate)

        async with get_async_session_context() as session:
            await breed_crud.create_multi(new_breeds, session)
            await cat_crud.create_multi(new_cats, session)

        logging.info('БД успешно заполнена тестовыми данными')


async def check_db_is_empty() -> bool:
    """Проверка БД на наличие записей."""
    async with get_async_session_context() as session:
        breeds = await breed_crud.get_breeds_list(session, limit=1, page=1)
        cats = await cat_crud.get_cats_list(session, limit=1, page=1)
    if breeds and cats:
        return False
    return True


def read_csv(
    filename: str, schema: BreedCreate | CatCreate
) -> list[BreedCreate | CatCreate]:
    """Чтение данных из csv файлов."""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(schema(**row))
    return data
