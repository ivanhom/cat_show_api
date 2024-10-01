from core.enums import CatColor, CatSex

BREED_API_URL = '/api/v1/breeds/'
CAT_API_URL = '/api/v1/cats/'

QUERY_LIMIT = 10
QUERY_PAGE = 1

BREED_SEARCH_DESCR = 'Строка для поиска породы по названию'
CAT_SEARCH_DESCR = 'Строка для поиска котёнка по имени или породе'
CAT_BREED_SEARCH_DESCR = 'Строка для поиска котёнка по ID породы'

QUERY_LIMIT_DESCR = 'Количество элементов в ответе'
PAGE_NUMBER_DESCR = 'Выбор страницы списка'

EXAMPLE_BREED_ID = 1
EXAMPLE_BREED_NAME = 'Русская голубая'
EXAMPLE_BREED_DESCR = ('Кошки породы русская голубая бывают среднего или '
                       'крупного размера. Имеют изящное тело и длинные, '
                       'стройные ноги. Эта кошка настолько грациозна, что '
                       'кажется, будто она передвигается на цыпочках.')

EXAMPLE_BREED_COUNT = 13
EXAMPLE_BREED_NEXT_URL = f'{BREED_API_URL}?limit=1&page=3'
EXAMPLE_BREED_PREV_URL = f'{BREED_API_URL}?limit=1&page=1'

EXAMPLE_CAT_ID = 1
EXAMPLE_CAT_NAME = 'Феликс'
EXAMPLE_CAT_DESCR = 'Ленивый домосед. Ласковый, когда голодный'
EXAMPLE_CAT_SEX = CatSex.male
EXAMPLE_CAT_AGE = 8
EXAMPLE_CAT_COLOR = CatColor.grey

EXAMPLE_CAT_COUNT = 35
EXAMPLE_CAT_NEXT_URL = f'{CAT_API_URL}?limit=1&page=3'
EXAMPLE_CAT_PREV_URL = f'{CAT_API_URL}?limit=1&page=1'

# Минимальный возраст котёнка для участия в выставках
CAT_MIN_AGE = 3
# Максимальный возраст котёнка для участия в выставках
CAT_MAX_AGE = 8

ERROR_BREED_EXISTS = 'Порода с таким именем уже существует в базе данных!'
ERROR_BREED_DOESNT_EXIST = 'Породы с таким ID не существует в базе данных!'
ERROR_CAT_DOESNT_EXIST = 'Котёнка с таким ID не существует в базе данных!'
