"""
Обработчики команды /start и основного меню
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.coffee_keyboards import main_menu_keyboard, coffee_menu_keyboard, collections_menu_keyboard
from keyboards.vinyl_keyboards import vinyl_menu_keyboard
from keyboards.books_keyboards import books_menu_keyboard
from keyboards.figures_keyboards import figures_menu_keyboard
from keyboards.plants_keyboards import plants_menu_keyboard
from keyboards.research_keyboards import research_menu_keyboard
from keyboards.projects_keyboards import projects_menu_keyboard

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


@router.message(F.text == "🎵 Винил")
async def vinyl_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления винилом"""
    await state.clear()

    await message.answer(
        "🎵 *Управление винилом*\n\n"
        "Здесь вы можете управлять коллекцией винила:\n"
        "• Добавлять новые записи\n"
        "• Указывать исполнителей, названия, годы\n"
        "• Управлять жанрами\n"
        "• Искать по коллекции\n\n"
        "Выберите действие:",
        reply_markup=vinyl_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "📚 Книги")
async def books_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления книгами"""
    await state.clear()

    await message.answer(
        "📚 *Управление книгами*\n\n"
        "Здесь вы можете управлять библиотекой:\n"
        "• Добавлять новые книги\n"
        "• Писать рецензии и мнения\n"
        "• Сохранять цитаты\n"
        "• Фильтровать по жанрам и языкам\n\n"
        "Выберите действие:",
        reply_markup=books_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "☕ Кофе")
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


@router.message(F.text == "🎭 Фигурки")
async def figures_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления фигурками"""
    await state.clear()

    await message.answer(
        "🎭 *Управление фигурками*\n\n"
        "Здесь вы можете управлять коллекцией фигурок:\n"
        "• Добавлять новые фигурки\n"
        "• Указывать бренды и названия\n"
        "• Фильтровать по брендам\n"
        "• Искать в коллекции\n\n"
        "Выберите действие:",
        reply_markup=figures_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "🌱 Растения")
async def plants_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления растениями"""
    await state.clear()

    await message.answer(
        "🌱 *Управление растениями*\n\n"
        "Здесь вы можете управлять коллекцией растений:\n"
        "• Добавлять новые растения\n"
        "• Указывать научные названия\n"
        "• Добавлять фотографии\n"
        "• Фильтровать по семействам и родам\n\n"
        "Выберите действие:",
        reply_markup=plants_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "📄 Исследования")
async def research_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления исследованиями"""
    await state.clear()

    await message.answer(
        "📄 *Управление исследованиями*\n\n"
        "Здесь вы можете управлять научными работами:\n"
        "• Добавлять публикации\n"
        "• Создавать инфографики\n"
        "• Указывать места публикации и годы\n"
        "• Просматривать статистику\n\n"
        "Выберите действие:",
        reply_markup=research_menu_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "🚀 Проекты")
async def projects_management(message: Message, state: FSMContext):
    """Обработчик кнопки управления проектами"""
    await state.clear()

    await message.answer(
        "🚀 *Управление проектами*\n\n"
        "Здесь вы можете управлять портфолио проектов:\n"
        "• Добавлять новые проекты\n"
        "• Писать описания\n"
        "• Управлять тегами\n"
        "• Фильтровать по технологиям\n\n"
        "Выберите действие:",
        reply_markup=projects_menu_keyboard(),
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
        reply_markup=collections_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "vinyl_menu")
async def show_vinyl_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления винилом"""
    await state.clear()

    await callback.message.edit_text(
        "🎵 *Управление винилом*\n\n"
        "Выберите действие:",
        reply_markup=vinyl_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "books_menu")
async def show_books_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления книгами"""
    await state.clear()

    await callback.message.edit_text(
        "📚 *Управление книгами*\n\n"
        "Выберите действие:",
        reply_markup=books_menu_keyboard(),
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


@router.callback_query(F.data == "figures_menu")
async def show_figures_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления фигурками"""
    await state.clear()

    await callback.message.edit_text(
        "🎭 *Управление фигурками*\n\n"
        "Выберите действие:",
        reply_markup=figures_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "plants_menu")
async def show_plants_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления растениями"""
    await state.clear()

    await callback.message.edit_text(
        "🌱 *Управление растениями*\n\n"
        "Выберите действие:",
        reply_markup=plants_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "research_menu")
async def show_research_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления исследованиями"""
    await state.clear()

    await callback.message.edit_text(
        "📄 *Управление исследованиями*\n\n"
        "Выберите действие:",
        reply_markup=research_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "projects_menu")
async def show_projects_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления проектами"""
    await state.clear()

    await callback.message.edit_text(
        "🚀 *Управление проектами*\n\n"
        "Выберите действие:",
        reply_markup=projects_menu_keyboard(),
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
