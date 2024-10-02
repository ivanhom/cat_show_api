from fastapi import FastAPI

from api import router
from core.config import settings
from core.init_db import fill_empty_db

app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(router)


@app.on_event('startup')
async def startup() -> None:
    """Вызов функции наполнения БД данными при старте
    приложения, если они отсутствует в БД.
    """
    await fill_empty_db()
