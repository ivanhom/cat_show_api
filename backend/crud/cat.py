from crud.base import CRUDBase
from models import Cat


class CRUDCat(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели Cat.
    """

    pass


cat_crud = CRUDCat(Cat)
