from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Breed(Base):
    """Модель для хранения породы котят в БД."""

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text(1000))

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'
