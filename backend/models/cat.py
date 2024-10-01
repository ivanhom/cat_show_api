from sqlalchemy.orm import Mapped

from core.db import Base


class Cat(Base):
    """Модель для хранения котят в БД."""

    name: Mapped[str]
