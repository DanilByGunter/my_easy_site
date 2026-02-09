"""
Главный файл Telegram-бота для управления данными сайта
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import start, coffee
from middlewares.auth import AdminMiddleware
from middlewares.error_handler import ErrorHandlerMiddleware, error_handler


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    # Настраиваем логгеры для aiogram
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)


async def main():
    """Основная функция запуска бота"""
    # Настраиваем логирование
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("🚀 Запуск Telegram-бота...")

    # Проверяем конфигурацию
    try:
        logger.info(f"Bot Token: {'*' * (len(config.bot_token) - 8)}{config.bot_token[-8:]}")
        logger.info(f"Admin ID: {config.admin_telegram_id}")
        logger.info(f"Database URL: {config.database_url[:20]}...")
        logger.info(f"Log Level: {config.log_level}")
    except Exception as e:
        logger.error(f"Ошибка конфигурации: {e}")
        sys.exit(1)

    # Создаем бота и диспетчер
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Используем MemoryStorage для FSM (в продакшене можно заменить на Redis)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем middleware
    dp.message.middleware(AdminMiddleware())
    dp.callback_query.middleware(AdminMiddleware())
    dp.message.middleware(ErrorHandlerMiddleware())
    dp.callback_query.middleware(ErrorHandlerMiddleware())

    # Регистрируем глобальный обработчик ошибок
    dp.errors.register(error_handler)

    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(coffee.router)

    logger.info("📝 Middleware и роутеры зарегистрированы")

    # Проверяем подключение к боту
    try:
        bot_info = await bot.get_me()
        logger.info(f"🤖 Бот запущен: @{bot_info.username} ({bot_info.full_name})")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Telegram API: {e}")
        sys.exit(1)

    # Проверяем подключение к базе данных
    try:
        from database import get_db_session
        async with get_db_session() as db:
            # Простая проверка подключения
            await db.execute("SELECT 1")
        logger.info("✅ Подключение к базе данных успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        sys.exit(1)

    # Уведомляем администратора о запуске
    if config.admin_telegram_id:
        try:
            await bot.send_message(
                config.admin_telegram_id,
                "🚀 *Бот запущен и готов к работе!*\n\n"
                f"🤖 Имя: {bot_info.full_name}\n"
                f"📱 Username: @{bot_info.username}\n"
                f"🔧 Версия: 1.0.0\n\n"
                "Используйте /start для начала работы.",
                parse_mode="Markdown"
            )
            logger.info("📨 Уведомление администратору отправлено")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось отправить уведомление администратору: {e}")

    logger.info("✅ Бот полностью инициализирован")

    try:
        # Запускаем polling
        logger.info("🔄 Начинаем polling...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("⏹️ Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        # Уведомляем администратора об остановке
        if config.admin_telegram_id:
            try:
                await bot.send_message(
                    config.admin_telegram_id,
                    "⏹️ *Бот остановлен*\n\n"
                    "Бот был корректно остановлен.",
                    parse_mode="Markdown"
                )
            except Exception:
                pass

        logger.info("🛑 Закрываем соединения...")
        await bot.session.close()
        logger.info("✅ Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        sys.exit(1)
