from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройка переменных окружения для backend."""

    app_title: str
    app_description: str
    database_url: str
    database_url_test: str = 'sqlite+aiosqlite:///./cat_show_test.db'

    class Config:
        env_file = '../infra/.env'
        extra = 'ignore'


settings = Settings()
