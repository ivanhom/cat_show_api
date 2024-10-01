from enum import StrEnum


class CatColor(StrEnum):
    """Цвета окраса котёнка."""

    black = 'Чёрный'
    white = 'Белый'
    grey = 'Серый'
    ginger = 'Рыжий'
    brown = 'Коричневый'
    blue = 'Голубой'
    mixed = 'Смешанный'


class CatSex(StrEnum):
    """Пол котёнка."""

    male = 'Мальчик'
    female = 'Девочка'
