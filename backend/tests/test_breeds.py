import pytest
from fastapi import status

from core.constants import (
    BREED_API_URL,
    ERROR_COUNT,
    ERROR_COUNT_LENGTH,
    ERROR_RESPONSE_SCHEMA,
    ERROR_STATUS_CODE,
)
from schemas.breed import BreedDB, BreedList
from tests.conftest import client

CREATE_BREED = {'name': 'Сфинкс', 'description': 'Короткошерстная порода'}
UPDATE_BREED = {'name': 'Британская', 'description': 'Пушистые и ласковые'}


def test_get_breeds_emty_list() -> None:
    """Вывод пустого списка пород."""
    response = client.get(BREED_API_URL)

    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)
    assert BreedList(**response.json()), ERROR_RESPONSE_SCHEMA


def test_create_breed() -> None:
    """Добавление новой породы."""
    response = client.post(BREED_API_URL, json=CREATE_BREED)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), ERROR_STATUS_CODE.format(status.HTTP_201_CREATED)
    assert BreedDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_create_breed_with_not_unique_name() -> None:
    """Попытка добавления породы с похожим названием."""
    response = client.post(BREED_API_URL, json=CREATE_BREED)
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), ERROR_STATUS_CODE.format(status.HTTP_400_BAD_REQUEST)


def test_get_breed_by_id() -> None:
    """Получение информации о породе по ID."""
    response = client.get(f'{BREED_API_URL}1/')
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)
    assert BreedDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_get_breed_by_wrong_id() -> None:
    """Попытка получения информации о породе по неверному ID."""
    response = client.get(f'{BREED_API_URL}100/')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), ERROR_STATUS_CODE.format(status.HTTP_404_NOT_FOUND)


def test_update_breed() -> None:
    """Редактирование информации о породе."""
    response = client.patch(f'{BREED_API_URL}1/', json=UPDATE_BREED)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), ERROR_STATUS_CODE.format(status.HTTP_201_CREATED)
    assert BreedDB(**response.json()), ERROR_RESPONSE_SCHEMA


def test_get_breeds() -> None:
    """Список всех пород."""
    client.post(BREED_API_URL, json=CREATE_BREED)

    response = client.get(BREED_API_URL)
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert BreedDB(**first_obj), ERROR_RESPONSE_SCHEMA


def test_get_breeds_by_breed_search() -> None:
    """Поиск пород по названию."""
    response = client.get(BREED_API_URL, params={'search': 'Сфинкс'})
    assert (
        response.status_code == status.HTTP_200_OK
    ), ERROR_STATUS_CODE.format(status.HTTP_200_OK)

    response = response.json()
    assert response.get('count') == len(
        response.get('results')
    ), ERROR_COUNT_LENGTH
    if response.get('count') != 0:
        first_obj = response.get('results')[0]
        assert BreedDB(**first_obj), ERROR_RESPONSE_SCHEMA
    assert response.get('count') == 1, ERROR_COUNT


def test_delete_breed() -> None:
    """Удаление породы."""
    response = client.delete(f'{BREED_API_URL}2/')
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), ERROR_STATUS_CODE.format(status.HTTP_204_NO_CONTENT)


def test_delete_breed_that_doesnt_exist() -> None:
    """Попытка удаления ранее удалённой породы."""
    response = client.delete(f'{BREED_API_URL}2/')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), ERROR_STATUS_CODE.format(status.HTTP_404_NOT_FOUND)

    client.post(BREED_API_URL, json=CREATE_BREED)
