import pytest
from fastapi import status

from core.constants import (
    CAT_API_URL,
    ERROR_COUNT,
    ERROR_COUNT_LENGTH,
    ERROR_RESPONSE_SCHEMA,
    ERROR_STATUS_CODE,
)
from core.enums import CatColor, CatSex
from schemas.cat import CatDB, CatList
from tests.conftest import client

CREATE_CAT = {
    'name': 'Васька',
    'description': 'Ленивый и голодный',
    'sex': CatSex.male,
    'months': 4,
    'color': CatColor.grey,
    'breed_id': 1,
}
UPDATE_CAT = {
    'name': 'Мурка',
    'description': 'Не распознаёт мышь',
    'sex': CatSex.female,
    'months': 6,
    'color': CatColor.white,
    'breed_id': 2,
}


def test_get_cats_emty_list() -> None:
    """Вывод пустого списка котят."""
    response = client.get(CAT_API_URL)

    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)
    assert CatList(**response.json()), ERROR_RESPONSE_SCHEMA


def test_create_cat() -> None:
    """Добавление нового котёнка."""
    response = client.post(CAT_API_URL, json=CREATE_CAT)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), ERROR_STATUS_CODE.format(status.HTTP_201_CREATED)
    assert CatDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_get_cat_by_id() -> None:
    """Получение информации о котёнке по ID."""
    response = client.get(f'{CAT_API_URL}1/')
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)
    assert CatDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_get_cat_by_wrong_id() -> None:
    """Попытка получения информации о котёнке по неверному ID."""
    response = client.get(f'{CAT_API_URL}100/')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), ERROR_STATUS_CODE.format(status.HTTP_404_NOT_FOUND)


def test_update_cat() -> None:
    """Редактирование информации о котёнке."""
    response = client.patch(f'{CAT_API_URL}1/', json=UPDATE_CAT)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), ERROR_STATUS_CODE.format(status.HTTP_201_CREATED)
    assert CatDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_get_cats() -> None:
    """Список всех котят."""
    client.post(CAT_API_URL, json=CREATE_CAT)

    response = client.get(CAT_API_URL)
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert CatDB(**first_obj), ERROR_RESPONSE_SCHEMA


def test_get_cats_by_name_search() -> None:
    """Поиск котят по имени."""
    response = client.get(CAT_API_URL, params={'search': 'Мурка'})
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert CatDB(**first_obj), ERROR_RESPONSE_SCHEMA
    assert response.get('count') == 1, ERROR_COUNT


def test_get_cats_by_breed_search() -> None:
    """Поиск котят по названию породы."""
    response = client.get(CAT_API_URL, params={'search': 'Сфинкс'})
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert CatDB(**first_obj), ERROR_RESPONSE_SCHEMA
    assert response.get('count') == 1, ERROR_COUNT


def test_get_cats_by_breed_id() -> None:
    """Поиск котят по ID породы."""
    response = client.get(CAT_API_URL, params={'breed_id': 1})
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert CatDB(**first_obj), ERROR_RESPONSE_SCHEMA
    assert response.get('count') == 1, ERROR_COUNT


def test_delete_cat() -> None:
    """Удаление котёнка."""
    response = client.delete(f'{CAT_API_URL}2/')
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), ERROR_STATUS_CODE.format(status.HTTP_204_NO_CONTENT)


def test_delete_cat_that_doesnt_exist() -> None:
    """Попытка удаления ранее удалённого котёнка."""
    response = client.delete(f'{CAT_API_URL}2/')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), ERROR_STATUS_CODE.format(status.HTTP_404_NOT_FOUND)
