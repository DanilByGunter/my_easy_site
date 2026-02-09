"""
Конфигурация Telegram-бота
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """Настройки Telegram-бота"""

    # Telegram Bot Token
    bot_token: str = ""

    # Admin Telegram ID для проверки прав доступа
    admin_telegram_id: Optional[int] = None

    # Database settings (используем те же что и backend)
    database_url: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    # Logging level
    log_level: str = "INFO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Получаем BOT_TOKEN из переменных окружения
        if not self.bot_token:
            self.bot_token = os.getenv("BOT_TOKEN", "")
            if not self.bot_token:
                raise ValueError("BOT_TOKEN не найден в переменных окружения")

        # Получаем ADMIN_TELEGRAM_ID
        if not self.admin_telegram_id:
            admin_id = os.getenv("ADMIN_TELEGRAM_ID")
            if admin_id:
                try:
                    self.admin_telegram_id = int(admin_id)
                except ValueError:
                    raise ValueError("ADMIN_TELEGRAM_ID должен быть числом")

        # Настройка базы данных (аналогично backend/app/settings.py)
        if not self.database_url:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                # Собираем из отдельных переменных
                self.postgres_user = os.getenv("POSTGRES_USER", "")
                self.postgres_password = os.getenv("POSTGRES_PASSWORD", "")
                self.postgres_db = os.getenv("POSTGRES_DB", "")

                if not all([self.postgres_user, self.postgres_password, self.postgres_db]):
                    raise ValueError(
                        "Параметры подключения к БД не найдены. "
                        "Установите POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB"
                    )

                database_url = (
                    f"postgresql+asyncpg://{self.postgres_user}:"
                    f"{self.postgres_password}@db:5432/{self.postgres_db}"
                )

            self.database_url = database_url

        # Уровень логирования
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        return self.admin_telegram_id is not None and user_id == self.admin_telegram_id


# Глобальный экземпляр конфигурации
config = BotConfig()
