from crud.base import CRUDBase
from models import Breed


class CRUDBreed(CRUDBase):
    """Класс для расширения стандартных
    CRUD операций с БД для модели Breed.
    """

    pass


breed_crud = CRUDBreed(Breed)
