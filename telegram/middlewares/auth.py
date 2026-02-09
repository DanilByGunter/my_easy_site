"""
Middleware для проверки авторизации администратора
"""
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from config import config

logger = logging.getLogger(__name__)


class AdminMiddleware(BaseMiddleware):
    """Middleware для проверки прав администратора"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем user_id из события
        user_id = None
        username = "Неизвестный"

        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            username = event.from_user.username or event.from_user.first_name or "Неизвестный"

        # Если не удалось получить user_id, блокируем
        if user_id is None:
            logger.warning("Не удалось получить user_id из события")
            return

        # Проверяем права администратора
        if not config.is_admin(user_id):
            logger.warning(f"Неавторизованная попытка доступа от {username} (ID: {user_id})")

            # Отправляем сообщение об отказе в доступе
            if isinstance(event, Message):
                await event.answer(
                    "❌ *Доступ запрещен*\n\n"
                    "Этот бот предназначен только для администратора сайта.",
                    parse_mode="Markdown"
                )
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Доступ запрещен", show_alert=True)

            return  # Блокируем выполнение handler'а

        # Если пользователь - администратор, продолжаем выполнение
        return await handler(event, data)
