"""
Обработчики для управления винилом
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import get_db_session
from services.vinyl_service import VinylService
from states.vinyl_states import VinylStates
from keyboards.vinyl_keyboards import (
    vinyl_menu_keyboard, genres_selection_keyboard,
    year_selection_keyboard, popular_genres_keyboard,
    cancel_keyboard, skip_keyboard, back_to_vinyl_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


# === ОСНОВНОЕ МЕНЮ ===

@router.callback_query(F.data == "vinyl_list")
async def show_vinyl_list(callback: CallbackQuery):
    """Показать список всего винила"""
    async with get_db_session() as db:
        service = VinylService(db)
        vinyl_records = await service.get_all_vinyl()

    if not vinyl_records:
        text = "📋 *Список винила*\n\n❌ Винил не найден"
    else:
        text = "📋 *Список винила:*\n\n"
        for i, vinyl in enumerate(vinyl_records, 1):
            text += f"{i}. *{vinyl.artist} - {vinyl.title}*"
            if vinyl.year:
                text += f" ({vinyl.year})"
            if vinyl.genres:
                genres_str = ", ".join(vinyl.genres[:3])  # Показываем только первые 3 жанра
                text += f"\n   🎭 {genres_str}"
                if len(vinyl.genres) > 3:
                    text += f" +{len(vinyl.genres) - 3}"
            text += "\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=vinyl_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "vinyl_add")
async def start_add_vinyl(callback: CallbackQuery, state: FSMContext):
    """Начать добавление нового винила"""
    await state.set_state(VinylStates.waiting_for_artist)

    await callback.message.edit_text(
        "➕ *Добавление нового винила*\n\n"
        "Введите имя исполнителя:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_artist)
async def process_artist(message: Message, state: FSMContext):
    """Обработать имя исполнителя"""
    artist = message.text.strip()

    if not artist:
        await message.answer(
            "❌ Имя исполнителя не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(artist=artist)
    await state.set_state(VinylStates.waiting_for_title)

    await message.answer(
        "🎵 *Название альбома*\n\n"
        "Введите название альбома:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )


@router.message(VinylStates.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Обработать название альбома"""
    title = message.text.strip()

    if not title:
        await message.answer(
            "❌ Название альбома не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(title=title)
    await state.set_state(VinylStates.waiting_for_year)

    await message.answer(
        "📅 *Год выпуска*\n\n"
        "Выберите год выпуска или введите вручную:",
        reply_markup=year_selection_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("select_year_"))
async def process_year_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор года"""
    year = int(callback.data.split("_")[-1])

    await state.update_data(year=year)
    await state.set_state(VinylStates.waiting_for_genres)

    await callback.message.edit_text(
        "🎭 *Жанры*\n\n"
        "Выберите жанры для альбома (можно выбрать несколько):",
        reply_markup=popular_genres_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "manual_year")
async def manual_year_input(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод года"""
    await callback.message.edit_text(
        "📅 *Год выпуска*\n\n"
        "Введите год выпуска (например: 1975):",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_year)
async def process_year_manual(message: Message, state: FSMContext):
    """Обработать год, введенный вручную"""
    try:
        year = int(message.text.strip())
        if year < 1900 or year > 2030:
            raise ValueError("Год вне допустимого диапазона")

        await state.update_data(year=year)
        await state.set_state(VinylStates.waiting_for_genres)

        await message.answer(
            "🎭 *Жанры*\n\n"
            "Выберите жанры для альбома (можно выбрать несколько):",
            reply_markup=popular_genres_keyboard(),
            parse_mode="Markdown"
        )
    except ValueError:
        await message.answer(
            "❌ Неверный формат года. Введите год от 1900 до 2030:",
            reply_markup=skip_keyboard()
        )


@router.callback_query(F.data.startswith("add_genre_"))
async def add_genre(callback: CallbackQuery, state: FSMContext):
    """Добавить жанр к альбому"""
    genre = callback.data.split("_", 2)[-1]

    data = await state.get_data()
    genres = data.get('genres', [])

    if genre not in genres:
        genres.append(genre)
        await state.update_data(genres=genres)

    # Обновляем сообщение с выбранными жанрами
    selected_text = f"Выбрано жанров: {len(genres)}\n" + ", ".join(genres) if genres else ""

    await callback.message.edit_text(
        f"🎭 *Жанры*\n\n"
        f"Выберите жанры для альбома (можно выбрать несколько):\n\n"
        f"{selected_text}",
        reply_markup=popular_genres_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer(f"Добавлен жанр: {genre}")


@router.callback_query(F.data == "genres_done")
async def finish_adding_vinyl(callback: CallbackQuery, state: FSMContext):
    """Завершить добавление винила"""
    data = await state.get_data()

    try:
        async with get_db_session() as db:
            service = VinylService(db)
            vinyl = await service.create_vinyl(
                artist=data['artist'],
                title=data['title'],
                year=data.get('year'),
                genres=data.get('genres', [])
            )
            await service.commit()

            # Форматируем информацию о созданном виниле
            info = "✅ *Винил добавлен!*\n\n"
            info += await service.format_vinyl_info(vinyl)

        await state.clear()

        await callback.message.edit_text(
            info,
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )

        logger.info(f"Добавлен новый винил: {vinyl.artist} - {vinyl.title}")

    except Exception as e:
        logger.error(f"Ошибка при добавлении винила: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при добавлении винила.",
            reply_markup=vinyl_menu_keyboard()
        )
        await state.clear()

    await callback.answer()


@router.callback_query(F.data == "skip_field")
async def skip_field(callback: CallbackQuery, state: FSMContext):
    """Пропустить поле"""
    current_state = await state.get_state()

    if current_state == VinylStates.waiting_for_year.state:
        await state.update_data(year=None)
        await state.set_state(VinylStates.waiting_for_genres)

        await callback.message.edit_text(
            "🎭 *Жанры*\n\n"
            "Выберите жанры для альбома (можно выбрать несколько):",
            reply_markup=popular_genres_keyboard(),
            parse_mode="Markdown"
        )

    await callback.answer("Поле пропущено")


# === ПОИСК И ФИЛЬТРАЦИЯ ===

@router.callback_query(F.data == "vinyl_search")
async def start_search(callback: CallbackQuery, state: FSMContext):
    """Начать поиск винила"""
    await state.set_state(VinylStates.waiting_for_search_query)

    await callback.message.edit_text(
        "🔍 *Поиск винила*\n\n"
        "Введите запрос для поиска (исполнитель или название):",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_search_query)
async def process_search(message: Message, state: FSMContext):
    """Обработать поисковый запрос"""
    query = message.text.strip()

    if not query:
        await message.answer(
            "❌ Запрос не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    async with get_db_session() as db:
        service = VinylService(db)
        results = await service.search_vinyl(query)

    await state.clear()

    if not results:
        text = f"🔍 *Результаты поиска: \"{query}\"*\n\n❌ Ничего не найдено"
    else:
        text = f"🔍 *Результаты поиска: \"{query}\"*\n\n"
        for i, vinyl in enumerate(results, 1):
            text += f"{i}. *{vinyl.artist} - {vinyl.title}*"
            if vinyl.year:
                text += f" ({vinyl.year})"
            text += "\n"

    await message.answer(
        text,
        reply_markup=back_to_vinyl_keyboard(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "vinyl_by_genre")
async def show_genres(callback: CallbackQuery):
    """Показать список жанров"""
    async with get_db_session() as db:
        service = VinylService(db)
        genres = await service.get_all_genres()

    if not genres:
        await callback.message.edit_text(
            "🎭 *Жанры*\n\n❌ Жанры не найдены",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "🎭 *Выберите жанр:*",
            reply_markup=genres_selection_keyboard(genres),
            parse_mode="Markdown"
        )

    await callback.answer()


@router.callback_query(F.data.startswith("select_genre_"))
async def show_vinyl_by_genre(callback: CallbackQuery):
    """Показать винил по жанру"""
    genre = callback.data.split("_", 2)[-1]

    async with get_db_session() as db:
        service = VinylService(db)
        vinyl_records = await service.get_vinyl_by_genre(genre)

    if not vinyl_records:
        text = f"🎭 *Жанр: {genre}*\n\n❌ Винил не найден"
    else:
        text = f"🎭 *Жанр: {genre}*\n\n"
        for i, vinyl in enumerate(vinyl_records, 1):
            text += f"{i}. *{vinyl.artist} - {vinyl.title}*"
            if vinyl.year:
                text += f" ({vinyl.year})"
            text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=back_to_vinyl_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


# === ОБЩИЕ ОБРАБОТЧИКИ ===

@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    """Отмена текущего действия"""
    await state.clear()

    await callback.message.edit_text(
        "❌ *Действие отменено*\n\n"
        "Выберите другое действие:",
        reply_markup=vinyl_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer("Действие отменено")
