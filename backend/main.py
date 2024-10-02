import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router
from core.config import settings
from core.init_db import fill_empty_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Вызов функции наполнения БД данными при старте
    приложения, если они отсутствует в БД.
    """
    asyncio.create_task(fill_empty_db())
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

app.include_router(router)


# @app.on_event('startup')
# async def startup() -> None:
#     """Вызов функции наполнения БД данными при старте
#     приложения, если они отсутствует в БД.
#     """
#     await fill_empty_db()
