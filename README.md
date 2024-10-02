# cat_show_api
API для администратора онлайн выставки котят.
Приложение хранит информацию о котятах и их породах.

Использованный стек технологий:

	• Python 3.11
	• FastAPI 0.111
	• Pydantic 2.7
	• PostgreSQL 15
	• SQLAlchemy 2
    • Alembic 1.13
    • Pytest 8.3
	• Docker, docker-compose

## 1. Настройка
### 1.1 Настройка после клонирования репозитория

Проект имеет следующую структуру:
- `backend` - директория для кода приложения Backend (FastAPI)
- `infra` - директория для настроек приложений и файлов развертывания инфраструктуры
- `requirements_style.txt` - файл с зависимостями для обеспечения единой 
  стилистики кода

В риложении подготовлены ряд файлов для первоначальной настройки:
- `requirements.txt` - зависимости для основного кода
- `.pre-commit-config.yaml` - настройки для проверки и исправления 
  (частично) стилистики
- `pyproject.toml` - настройки для стилизатора `black`
- `setup.cfg` - настройки для `flake8` и `isort`

После клонирования репозитория устанавливаем и настраиваем 
виртуальное окружение для приложения:

1. Переходим в директорию `/backend`
2. Устанавливаем и активируем виртуальное окружение
    - Для linux/mac:
      ```shell
      python3.11 -m venv .backend_venv
      source .backend_venv/bin/activate
      ```
    - Для Windows:
      ```shell
      py -3.11 -m venv .backend_venv
      .\.backend_venv\Scripts\activate
      ```
    В начале командной строки должно появиться название виртуального окружения `(.backend_venv)`

    Директория `.backend_venv` уже прописана в настройках git и стилизатора в 
    качестве исключения
3. Обновляем менеджер пакетов `pip` (по желанию)
    ```shell
    python3 -m pip install --upgrade pip
    ```
4. Устанавливаем основные зависимости и зависимости для стилистики
    ```shell
    pip install -r requirements.txt
    pip install -r ../requirements_style.txt
    ```

### 1.2 Проверка и фиксация стилистики

Для проверки и фиксации стилей перед итоговым коммитом:
1. Проверяем что находимся в корневой директории приложения `backend`
2. Выполняем команду
    ```shell
    pre-commit run --all-files
    ```
    Возможно потребуется запуск несколько раз.
    В итоге должен получиться примерно такой вывод:
    ```
    isort.............Passed
    black.............Passed
    flake8............Passed
    ```
   
### 1.3 Запуск приложения

Перед запуском приложений убеждаемся, что находимся в корневой директории 
приложения `backend`

При запуске отладки в IDE дополнительно проверяем, что бы корневая директория 
приложения была установлена в качестве рабочего каталога.

Для VSCode файл запуска дебагера выглядит примерно так (при условии, что 
главный файл приложения называется `main.py`):
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Backend Debugger",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload"
            ],
            "jinja": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

Для PyCharm установить параметр `Working directory`

## 1.4 Структура репозитория

```shell
wb_bears
│
├── backend/                            # Директория для бэкенда
│   ├── alembic/                        # Каталог для файлов Allembic
│   ├── api/                            # Каталог для API маршрутов
│   │   ├── api_v1/                     # Каталог для маршрутов API версии 1
│   │   │   ├── __init__.py             
│   │   │   ├── breed.py                # Эндпоинты для работы с породами
│   │   │   └── cat.py                  # Эндпоинты для работы с котятами
│   │   ├── __init__.py                 
│   │   ├── pagination.py               # Пагинация для данных API
│   │   └── validators.py               # Валидаторы для данных API
│   ├── core/                           # Основные настройки и конфигурации
│   │   ├── __init__.py                 
│   │   ├── base.py                     # Импорты моделей для Alembic
│   │   ├── config.py                   # Конфигурационные параметры приложения
│   │   ├── constants.py                # Константы для приложения
│   │   ├── db.py                       # Базовая модель для SQLAlchemy
│   │   ├── enums.py                    # Enum модели
│   │   └── init_db.py                  # Первичное заполнение БД подготовленными данными
│   ├── crud/                           
│   │   ├── __init__.py                 
│   │   ├── base.py                     # Базовые CRUD операции для СУБД
│   │   ├── breed.py                    # CRUD операции для модели Breed
│   │   └── cat.py                      # CRUD операции для модели Cat
│   ├── models/                         # Модели для СУБД
│   │   ├── __init__.py                 
│   │   ├── breed.py                    # Модель Breed для ДБ
│   │   └── cat.py                      # Модель Cat для ДБ
│   ├── schemas/                        # Pydantic схемы
│   │   ├── __init__.py                 
│   │   ├── breed.py                    # Схемы для модели Breed 
│   │   └── cat.py                      # Схемы для модели Cat 
│   ├── start_data/                     # Подготовленные данные для БД
│   │   ├── breeds_data.csv             # Данные для пород
│   │   └── cats_data.csv               # Данные для котят
│   ├── tests/                          # Тесты для API приложения
│   │   ├── conftest.py                 # Фикстуры для pytest
│   │   ├── test_breeds.py              # Тесты для API эндпоинтов breeds
│   │   └── test_cats.py                # Тесты для API эндпоинтов cats
│   ├── .dockerignore                   # Файл игнорирования Docker
│   ├── .pre-commit-config.yaml         # Конфигурация для pre-commit hooks
│   ├── alembic.ini                     # Файл конфигурации для Alembic
│   ├── docker-entrypoint.bash          # Скрипт входной точки для Docker
│   ├── Dockerfile                      # Файл описания образа Docker
│   ├── main.py                         # Главная точка входа для запуска приложения
│   ├── pyproject.toml                  # Конфигурационный файл для black форматтера
│   ├── requirements.txt                # Зависимости для backend
│   └── setup.cfg                       # Конфигурационный файл для setuptools
│
├── infra/                              # Директория для инфраструктурных файлов
│   ├── env.example                     # Пример файла окружения
│   ├── docker-compose.yml              # Файл описания сервисов Docker Compose
│   └── nginx.conf                      # Конфигурация веб-сервера Nginx
│
├── .gitignore                          # Файл, определяющий, какие файлы и директории игнорировать в Git
├── README.md                           # Файл документации проекта
└── requirements_style.txt              # Зависимости для стилей кода
```

## 2. Запуск приложения
### 2.1 Запуск приложения локально

1. Создать `infra/.env` на основе `infra/.env.example` Указав валидные данные для подключения.


```ini
      # backend
      APP_TITLE=Выставка котят  # Имя бекенд приложения по-умолчанию
      APP_DESCRIPTION=API для администратора онлайн выставки котят  # Описание бекенд приложения по-умолчанию

      # SQLite database
      # DATABASE_URL="sqlite+aiosqlite:///./cat_show.db"  # Локальная БД для отладки
      
      # Postgresql database
      POSTGRES_USER=your_db_username  # Имя администратора БД
      POSTGRES_PASSWORD=your_db_password  # Пароль администратора БД
      POSTGRES_DB=cat_show  # Имя БД 
      POSTGRES_SERVER=db  # Имя хоста подключения к БД
      POSTGRES_PORT=5432  # Номер порта подключения к БД
      # Строка подключения к БД, формируемая из переменных описанных выше
      DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:${POSTGRES_PORT}/${POSTGRES_DB}
      
      # SQLite database for TESTING
      DATABASE_URL_TEST="sqlite+aiosqlite:///./cat_show_test.db"  # Локальная БД для тестирования

```

2. Запустить `docker-compose up -d --build`.
3. Сервер будет доступен по адресу `http://localhost:8000`
4. Документация Swagger будет доступен по адресу `http://localhost:8000/docs`
5. При первом запуске в базу данных будут автоматически записаны начальные данные
6. Для запуска тестов необходимо выполнить в терминале команду `pytest`, находясь в директории 
приложения `backend` 
