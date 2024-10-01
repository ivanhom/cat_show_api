from typing import AsyncGenerator

from sqlalchemy import String, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declarative_base, declared_attr, Mapped, mapped_column, sessionmaker
)

from core.config import settings


class PreBase:
    """Базовая модель для БД."""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)

    @declared_attr
    def __tablename__(cls) -> str:
        """Сохранение имени таблицы в БД в нижнем регистре."""
        return cls.__name__.lower()

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция-генератор для получения асинхронной сессии доступа к БД."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
