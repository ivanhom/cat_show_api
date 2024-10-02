from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import CatColor, CatSex
from crud.base import CRUDBase
from models import Breed, Cat


class CRUDCat(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели Cat.
    """

    async def get_cats_list(
        self,
        session: AsyncSession,
        search: str | None = None,
        breed_id: int | None = None,
        sex: list[CatSex] = [],
        color: list[CatColor] = [],
        limit: int = 10,
        page: int = 1,
    ) -> tuple[list[Cat], int]:
        """Получает из базы данных список котят по запрашиваемым параметрам
        в соответствии с пагинацией, а также общее количество котят,
        удовлетворяющих запрашиваемым параметром без пагинации.
        """

        query = select(Cat)

        if search is not None:
            query = query.join(Breed).where(
                or_(
                    Cat.name.ilike(f'%{search}%'),
                    Breed.name.ilike(f'%{search}%'),
                )
            )
        if breed_id is not None:
            query = query.where(Cat.breed_id == breed_id)
        if sex:
            query = query.where(Cat.sex.in_(sex))
        if color:
            query = query.where(Cat.color.in_(color))

        total_cats = await session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total_count = total_cats.scalar()

        cats = await session.execute(
            query.offset((page - 1) * limit).limit(limit).order_by(Cat.name)
        )
        cats_list = cats.scalars().all()

        return cats_list, total_count


cat_crud = CRUDCat(Cat)
