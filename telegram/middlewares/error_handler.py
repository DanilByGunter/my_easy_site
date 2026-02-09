"""
Middleware для обработки ошибок
"""
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, ErrorEvent
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseMiddleware):
    """Middleware для централизованной обработки ошибок"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except TelegramBadRequest as e:
            logger.error(f"Telegram Bad Request: {e}")
            await self._send_error_message(event, "❌ Ошибка запроса к Telegram API")
        except TelegramForbiddenError as e:
            logger.error(f"Telegram Forbidden: {e}")
            # Не отправляем сообщение, так как бот заблокирован
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await self._send_error_message(event, "❌ Ошибка базы данных. Попробуйте позже.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            await self._send_error_message(event, "❌ Произошла неожиданная ошибка")

    async def _send_error_message(self, event: TelegramObject, message: str):
        """Отправить сообщение об ошибке пользователю"""
        try:
            if isinstance(event, Message):
                await event.answer(message)
            elif isinstance(event, CallbackQuery):
                await event.answer(message, show_alert=True)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")


async def error_handler(event: ErrorEvent):
    """Глобальный обработчик ошибок для aiogram"""
    logger.error(f"Critical error: {event.exception}", exc_info=True)

    # Попытаемся уведомить пользователя
    if event.update.message:
        try:
            await event.update.message.answer(
                "❌ Произошла критическая ошибка. Администратор уведомлен."
            )
        except Exception:
            pass
    elif event.update.callback_query:
        try:
            await event.update.callback_query.answer(
                "❌ Критическая ошибка",
                show_alert=True
            )
        except Exception:
            pass
