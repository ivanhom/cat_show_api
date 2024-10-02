import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from core.config import settings
from core.db import Base, get_async_session
from main import app

engine_test = create_async_engine(
    settings.database_url_test, poolclass=NullPool
)
AsyncSessionLocal = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция-генератор для получения асинхронной сессии тестов БД."""
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> None:
    """Создание и удаление таблиц в БД при запуске тестов."""

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Создание экземпляра стандартного цикла событий
    для каждого тестового случая.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания асинхронного клиента тестирования."""
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
