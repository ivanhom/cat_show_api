from core.enums import CatColor, CatSex

EXAMPLE_BREED_ID = 1
EXAMPLE_BREED_NAME = 'Русская голубая'
EXAMPLE_BREED_DESCR = ('Кошки породы русская голубая бывают среднего или '
                       'крупного размера. Имеют изящное тело и длинные, '
                       'стройные ноги. Эта кошка настолько грациозна, что '
                       'кажется, будто она передвигается на цыпочках.')

EXAMPLE_CAT_ID = 1
EXAMPLE_CAT_NAME = 'Феликс'
EXAMPLE_CAT_DESCR = 'Ленивый домосед. Ласковый, когда голодный'
EXAMPLE_CAT_SEX = CatSex.male
EXAMPLE_CAT_AGE = 8
EXAMPLE_CAT_COLOR = CatColor.grey

# Минимальный возраст котёнка для участия в выставках
CAT_MIN_AGE = 3
# Максимальный возраст котёнка для участия в выставках
CAT_MAX_AGE = 8

ERROR_BREED_EXISTS = 'Порода с таким именем уже существует в базе данных!'
ERROR_BREED_DOESNT_EXIST = 'Породы с таким ID не существует в базе данных!'
ERROR_CAT_DOESNT_EXIST = 'Котёнка с таким ID не существует в базе данных!'
