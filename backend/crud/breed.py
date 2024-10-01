from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Breed


class CRUDBreed(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели Breed.
    """

    async def get_breeds_list(
        self,
        session: AsyncSession,
        search: str | None,
        limit: int,
        page: int,
    ) -> tuple[list[Breed], int]:
        """Получает из базы данных список пород по запрашиваемым параметрам
        в соответствии с пагинацией, а также общее количество пород,
        удовлетворяющих запрашиваемым параметром без пагинации.
        """

        query = select(Breed)

        if search is not None:
            query = query.where(Breed.name.ilike(f'%{search}%'))

        total_breeds = await session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total_count = total_breeds.scalar()

        breeds = await session.execute(
            query.offset((page - 1) * limit).limit(limit).order_by(Breed.name)
        )
        breeds_list = breeds.scalars().all()

        return breeds_list, total_count


breed_crud = CRUDBreed(Breed)
