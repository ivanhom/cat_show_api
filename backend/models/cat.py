from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.enums import CatColor, CatSex


class Cat(Base):
    """Модель для хранения котят в БД."""

    sex: Mapped[CatSex]
    color: Mapped[CatColor]
    months: Mapped[int]
    breed_id: Mapped[int] = mapped_column(
        ForeignKey('breed.id', ondelete='SET NULL'), nullable=True
    )

    breed: Mapped['Breed'] = relationship(
        back_populates='cats', lazy='selectin'
    )
