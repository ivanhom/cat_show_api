from sqlalchemy.orm import Mapped, relationship

from core.db import Base


class Breed(Base):
    """Модель для хранения породы котят в БД."""

    cats: Mapped[list['Cat']] = relationship(back_populates='breed')
