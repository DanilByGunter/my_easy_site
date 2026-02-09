"""
Обработчики команды /start и основного меню
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.coffee_keyboards import main_menu_keyboard, coffee_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    username = message.from_user.username or "Неизвестный"

    logger.info(f"Администратор {username} запустил бота")

    # Очищаем состояние при старте
    await state.clear()

    # Приветствуем администратора
    await message.answer(
        f"👋 *Добро пожаловать, {username}!*\n\n"
        "🤖 Это бот для управления данными вашего сайта.\n"
        "Здесь вы можете добавлять, редактировать и удалять информацию о кофе, "
        "книгах, винилах и других коллекциях.\n\n"
        "📱 Выберите раздел для работы:",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "☕ Управление кофе")
async def coffee_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления кофе"""
    await state.clear()

    await message.answer(
        "☕ *Управление кофе*\n\n"
        "Здесь вы можете управлять информацией о кофе:\n"
        "• Добавлять и редактировать бренды\n"
        "• Добавлять новые сорта кофе\n"
        "• Писать отзывы и оценки\n\n"
        "Выберите действие:",
        reply_markup=coffee_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message):
    """Показать статистику"""
    # TODO: Реализовать статистику
    await message.answer(
        "📊 *Статистика*\n\n"
        "🚧 Раздел в разработке...\n"
        "Здесь будет отображаться статистика по всем коллекциям.",
        parse_mode="Markdown"
    )


@router.message(F.text == "❓ Помощь")
async def show_help(message: Message):
    """Показать помощь"""
    await message.answer(
        "❓ *Помощь*\n\n"
        "*Доступные команды:*\n"
        "• /start - Перезапустить бота\n"
        "• /help - Показать эту справку\n\n"
        "*Разделы:*\n"
        "• ☕ Управление кофе - Добавление и редактирование информации о кофе\n"
        "• 📊 Статистика - Просмотр статистики коллекций\n\n"
        "*Как пользоваться:*\n"
        "1. Выберите нужный раздел в главном меню\n"
        "2. Следуйте инструкциям бота\n"
        "3. Используйте кнопки для навигации\n\n"
        "При возникновении проблем перезапустите бота командой /start",
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()

    await callback.message.edit_text(
        "🏠 *Главное меню*\n\n"
        "Выберите раздел для работы:",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "coffee_menu")
async def show_coffee_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления кофе"""
    await state.clear()

    await callback.message.edit_text(
        "☕ *Управление кофе*\n\n"
        "Выберите действие:",
        reply_markup=coffee_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    """Отмена текущего действия"""
    await state.clear()

    await callback.message.edit_text(
        "❌ *Действие отменено*\n\n"
        "Выберите другое действие:",
        reply_markup=coffee_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer("Действие отменено")
