from fastapi import FastAPI

from api import router
from core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(router)
