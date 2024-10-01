def get_next_and_previous_urls(
    current_api_url: str,
    total_count: int,
    limit: int,
    page: int,
    **kwargs,
) -> tuple[str | None, str | None]:
    """
     Генерирует URL-адреса для следующей и предыдущей
     страниц при использовании пагинации.

     Эта функция принимает текущий URL API и параметры пагинации,
     а затем возвращает URL-адреса для следующей и предыдущей страниц
     с учетом переданных параметров.

     Параметры:
     - current_api_url (str): Строка с текущим URL API, к которому
     будут добавлены параметры запроса.
     - total_count (int): Общее количество результатов, которые база
     данных может выдать на запрос.
     - limit (int): Максимальное количество результатов на одной странице.
     - page (int): Номер текущей страницы.
     - **kwargs: Остальные параметры запроса к ендпоинту,
    передаваемые как именные аргументы.

     Возвращает:
     tuple[str | None, str | None]: Кортеж, содержащий URL-адреса
     для следующей и предыдущей страниц.
     Если соответствующая страница отсутствует,
     возвращает None для этой страницы.

     Примеры использования:
     get_next_and_previous_urls(
         'http://api.example.com/items', 100, 10, 1, search='query')
     >>> ('http://api.example.com/items?limit=10&page=2&search=query', None)

     get_next_and_previous_urls(
         'http://api.example.com/items', 100, 10, 2, search='query')
     >>> ('http://api.example.com/items?limit=10&page=3&search=query',
     >>>  'http://api.example.com/items?limit=10&page=1&search=query')
    """
    next_page = page + 1 if (page * limit) < total_count else None
    previous_page = page - 1 if page > 1 else None

    next_url = (
        (current_api_url + f'?limit={limit}&page={next_page}')
        if next_page
        else None
    )
    prev_url = (
        (current_api_url + f'?limit={limit}&page={previous_page}')
        if previous_page
        else None
    )

    for key, value in kwargs.items():
        if value is not None and next_url:
            if type(value) is not list:
                next_url += f'&{key}={value}'
            else:
                for i in value:
                    next_url += f'&{key}={i}'

        if value is not None and prev_url:
            if type(value) is not list:
                prev_url += f'&{key}={value}'
            else:
                for i in value:
                    prev_url += f'&{key}={i}'

    return next_url, prev_url
