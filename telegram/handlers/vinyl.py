"""
Обработчики для управления винилом
"""
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import get_db_session
from services.vinyl_service import VinylService
from services.s3_service import S3Service
from states.vinyl_states import VinylStates
from keyboards.vinyl_keyboards import (
    vinyl_menu_keyboard, vinyl_selection_keyboard, vinyl_edit_fields_keyboard,
    year_selection_keyboard, popular_genres_keyboard, confirm_delete_keyboard,
    cancel_keyboard, skip_keyboard, photo_upload_keyboard
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


@router.callback_query(F.data == "manual_year", VinylStates.waiting_for_year)
async def manual_year_input(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод года при добавлении"""
    await callback.message.edit_text(
        "📅 *Год выпуска*\n\n"
        "Введите год выпуска (например: 1975):",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "manual_year", VinylStates.waiting_for_edit_year)
async def manual_year_input_edit(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод года при редактировании"""
    await callback.message.edit_text(
        "📅 *Редактирование года*\n\n"
        "Введите новый год выпуска (например: 1975):",
        reply_markup=cancel_keyboard(),
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


@router.callback_query(F.data.startswith("add_genre_"), VinylStates.waiting_for_genres)
async def add_genre(callback: CallbackQuery, state: FSMContext):
    """Добавить жанр к альбому при добавлении"""
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


@router.callback_query(F.data == "genres_done", VinylStates.waiting_for_genres)
async def ask_for_photo(callback: CallbackQuery, state: FSMContext):
    """Запросить фото альбома при добавлении"""
    await state.set_state(VinylStates.waiting_for_photo)

    await callback.message.edit_text(
        "📸 *Фото альбома*\n\n"
        "Отправьте фото обложки альбома или пропустите этот шаг:",
        reply_markup=photo_upload_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    """Обработать загруженное фото"""
    # Получаем самое большое фото
    photo = message.photo[-1]

    # Загружаем фото в S3
    s3_service = S3Service()
    photo_url = await s3_service.upload_photo(bot, photo, "vinyl")

    if photo_url:
        await state.update_data(photo_url=photo_url)
        await message.answer("📸 Фото успешно загружено!")
    else:
        await message.answer("⚠️ Не удалось загрузить фото, но винил будет добавлен без фото.")

    await finish_adding_vinyl_with_data(message, state)


@router.callback_query(F.data == "skip_photo", VinylStates.waiting_for_photo)
async def skip_photo(callback: CallbackQuery, state: FSMContext):
    """Пропустить загрузку фото при добавлении"""
    await finish_adding_vinyl_with_data(callback.message, state)
    await callback.answer("Фото пропущено")


async def finish_adding_vinyl_with_data(message: Message, state: FSMContext):
    """Завершить добавление винила с данными"""
    data = await state.get_data()

    # Проверяем наличие обязательных полей
    if not data.get('artist') or not data.get('title'):
        logger.error(f"Отсутствуют обязательные данные для создания винила: {data}")
        try:
            await message.edit_text(
                "❌ Ошибка: отсутствуют данные об исполнителе или названии альбома.",
                reply_markup=vinyl_menu_keyboard()
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Ошибка: отсутствуют данные об исполнителе или названии альбома.",
                reply_markup=vinyl_menu_keyboard()
            )
        await state.clear()
        return

    try:
        async with get_db_session() as db:
            service = VinylService(db)
            vinyl = await service.create_vinyl(
                artist=data['artist'],
                title=data['title'],
                year=data.get('year'),
                genres=data.get('genres', []),
                photo_url=data.get('photo_url')
            )
            await service.commit()

            # Форматируем информацию о созданном виниле
            info = "✅ *Винил добавлен!*\n\n"
            info += await service.format_vinyl_info(vinyl)

        await state.clear()

        # Безопасное редактирование сообщения
        try:
            await message.edit_text(
                info,
                reply_markup=vinyl_menu_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as edit_error:
            # Если не удалось отредактировать, отправляем новое сообщение
            logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
            await message.answer(
                info,
                reply_markup=vinyl_menu_keyboard(),
                parse_mode="Markdown"
            )

        logger.info(f"Добавлен новый винил: {vinyl.artist} - {vinyl.title}")

    except Exception as e:
        logger.error(f"Ошибка при добавлении винила: {e}")
        # Безопасное редактирование сообщения об ошибке
        try:
            await message.edit_text(
                "❌ Произошла ошибка при добавлении винила.",
                reply_markup=vinyl_menu_keyboard()
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Произошла ошибка при добавлении винила.",
                reply_markup=vinyl_menu_keyboard()
            )
        await state.clear()


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
    elif current_state == VinylStates.waiting_for_edit_year.state:
        # При редактировании года - пропускаем (оставляем текущий год)
        await update_vinyl_field(callback.message, state)

    await callback.answer("Поле пропущено")


# === УДАЛЕНИЕ ВИНИЛА ===

@router.callback_query(F.data == "vinyl_delete")
async def start_delete_vinyl(callback: CallbackQuery, state: FSMContext):
    """Начать удаление винила"""
    async with get_db_session() as db:
        service = VinylService(db)
        vinyl_records = await service.get_all_vinyl()

    if not vinyl_records:
        await callback.message.edit_text(
            "🗑️ *Удаление винила*\n\n❌ Винил не найден",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    await state.set_state(VinylStates.waiting_for_delete_selection)

    await callback.message.edit_text(
        "🗑️ *Удаление винила*\n\n"
        "Выберите винил для удаления:",
        reply_markup=vinyl_selection_keyboard(vinyl_records),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_vinyl_"), VinylStates.waiting_for_delete_selection)
async def confirm_delete_vinyl(callback: CallbackQuery, state: FSMContext):
    """Подтвердить удаление винила"""
    vinyl_id = callback.data.split("_")[-1]

    async with get_db_session() as db:
        service = VinylService(db)
        vinyl = await service.get_vinyl_by_id(vinyl_id)

    if not vinyl:
        await callback.message.edit_text(
            "❌ Винил не найден",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return

    await state.update_data(vinyl_id=vinyl_id)
    await state.set_state(VinylStates.waiting_for_delete_confirmation)

    info = await VinylService(None).format_vinyl_info(vinyl)
    await callback.message.edit_text(
        f"🗑️ *Удаление винила*\n\n"
        f"{info}\n"
        f"❓ Вы уверены, что хотите удалить этот винил?",
        reply_markup=confirm_delete_keyboard(vinyl_id),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_vinyl_"))
async def delete_vinyl_confirmed(callback: CallbackQuery, state: FSMContext):
    """Удалить винил после подтверждения"""
    vinyl_id = callback.data.split("_")[-1]

    try:
        async with get_db_session() as db:
            service = VinylService(db)
            success = await service.delete_vinyl(vinyl_id)

            if success:
                await service.commit()
                await callback.message.edit_text(
                    "✅ *Винил успешно удален!*",
                    reply_markup=vinyl_menu_keyboard(),
                    parse_mode="Markdown"
                )
                logger.info(f"Удален винил с ID: {vinyl_id}")
            else:
                await callback.message.edit_text(
                    "❌ Винил не найден или уже удален",
                    reply_markup=vinyl_menu_keyboard(),
                    parse_mode="Markdown"
                )

    except Exception as e:
        logger.error(f"Ошибка при удалении винила: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при удалении винила",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )

    await state.clear()
    await callback.answer()


# === РЕДАКТИРОВАНИЕ ВИНИЛА ===

@router.callback_query(F.data == "vinyl_edit")
async def start_edit_vinyl(callback: CallbackQuery, state: FSMContext):
    """Начать редактирование винила"""
    async with get_db_session() as db:
        service = VinylService(db)
        vinyl_records = await service.get_all_vinyl()

    if not vinyl_records:
        await callback.message.edit_text(
            "✏️ *Редактирование винила*\n\n❌ Винил не найден",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    await state.set_state(VinylStates.waiting_for_vinyl_selection)

    await callback.message.edit_text(
        "✏️ *Редактирование винила*\n\n"
        "Выберите винил для редактирования:",
        reply_markup=vinyl_selection_keyboard(vinyl_records),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_vinyl_"), VinylStates.waiting_for_vinyl_selection)
async def select_edit_field(callback: CallbackQuery, state: FSMContext):
    """Выбрать поле для редактирования"""
    vinyl_id = callback.data.split("_")[-1]

    async with get_db_session() as db:
        service = VinylService(db)
        vinyl = await service.get_vinyl_by_id(vinyl_id)

    if not vinyl:
        await callback.message.edit_text(
            "❌ Винил не найден",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return

    await state.update_data(vinyl_id=vinyl_id)
    await state.set_state(VinylStates.waiting_for_edit_field_selection)

    info = await VinylService(None).format_vinyl_info(vinyl)
    await callback.message.edit_text(
        f"✏️ *Редактирование винила*\n\n"
        f"{info}\n"
        f"Выберите поле для редактирования:",
        reply_markup=vinyl_edit_fields_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


# === ОБРАБОТЧИКИ РЕДАКТИРОВАНИЯ ПОЛЕЙ ===

@router.callback_query(F.data == "edit_vinyl_artist")
async def edit_artist(callback: CallbackQuery, state: FSMContext):
    """Редактировать исполнителя"""
    await state.set_state(VinylStates.waiting_for_edit_artist)

    await callback.message.edit_text(
        "🎤 *Редактирование исполнителя*\n\n"
        "Введите нового исполнителя:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_edit_artist)
async def process_edit_artist(message: Message, state: FSMContext):
    """Обработать нового исполнителя"""
    artist = message.text.strip()

    if not artist:
        await message.answer(
            "❌ Имя исполнителя не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await update_vinyl_field(message, state, artist=artist)


@router.callback_query(F.data == "edit_vinyl_title")
async def edit_title(callback: CallbackQuery, state: FSMContext):
    """Редактировать название"""
    await state.set_state(VinylStates.waiting_for_edit_title)

    await callback.message.edit_text(
        "🎵 *Редактирование названия*\n\n"
        "Введите новое название альбома:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_edit_title)
async def process_edit_title(message: Message, state: FSMContext):
    """Обработать новое название"""
    title = message.text.strip()

    if not title:
        await message.answer(
            "❌ Название альбома не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await update_vinyl_field(message, state, title=title)


@router.callback_query(F.data == "edit_vinyl_year")
async def edit_year(callback: CallbackQuery, state: FSMContext):
    """Редактировать год"""
    await state.set_state(VinylStates.waiting_for_edit_year)

    await callback.message.edit_text(
        "📅 *Редактирование года*\n\n"
        "Выберите новый год выпуска или введите вручную:",
        reply_markup=year_selection_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_year_"), VinylStates.waiting_for_edit_year)
async def process_edit_year_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор года при редактировании"""
    year = int(callback.data.split("_")[-1])
    await update_vinyl_field(callback.message, state, year=year)
    await callback.answer()


@router.message(VinylStates.waiting_for_edit_year)
async def process_edit_year_manual(message: Message, state: FSMContext):
    """Обработать год, введенный вручную при редактировании"""
    try:
        year = int(message.text.strip())
        if year < 1900 or year > 2030:
            raise ValueError("Год вне допустимого диапазона")

        await update_vinyl_field(message, state, year=year)
    except ValueError:
        await message.answer(
            "❌ Неверный формат года. Введите год от 1900 до 2030:",
            reply_markup=cancel_keyboard()
        )


@router.callback_query(F.data == "edit_vinyl_genres")
async def edit_genres(callback: CallbackQuery, state: FSMContext):
    """Редактировать жанры"""
    await state.set_state(VinylStates.waiting_for_edit_genres)
    await state.update_data(genres=[])  # Сбрасываем жанры

    await callback.message.edit_text(
        "🎭 *Редактирование жанров*\n\n"
        "Выберите новые жанры для альбома (можно выбрать несколько):",
        reply_markup=popular_genres_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("add_genre_"), VinylStates.waiting_for_edit_genres)
async def add_genre_edit(callback: CallbackQuery, state: FSMContext):
    """Добавить жанр при редактировании"""
    genre = callback.data.split("_", 2)[-1]

    data = await state.get_data()
    genres = data.get('genres', [])

    if genre not in genres:
        genres.append(genre)
        await state.update_data(genres=genres)

    # Обновляем сообщение с выбранными жанрами
    selected_text = f"Выбрано жанров: {len(genres)}\n" + ", ".join(genres) if genres else ""

    await callback.message.edit_text(
        f"🎭 *Редактирование жанров*\n\n"
        f"Выберите новые жанры для альбома (можно выбрать несколько):\n\n"
        f"{selected_text}",
        reply_markup=popular_genres_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer(f"Добавлен жанр: {genre}")


@router.callback_query(F.data == "genres_done", VinylStates.waiting_for_edit_genres)
async def finish_edit_genres(callback: CallbackQuery, state: FSMContext):
    """Завершить редактирование жанров"""
    data = await state.get_data()
    genres = data.get('genres', [])
    await update_vinyl_field(callback.message, state, genres=genres)
    await callback.answer()


@router.callback_query(F.data == "edit_vinyl_photo")
async def edit_photo(callback: CallbackQuery, state: FSMContext):
    """Редактировать фото"""
    await state.set_state(VinylStates.waiting_for_edit_photo)

    await callback.message.edit_text(
        "📸 *Редактирование фото*\n\n"
        "Отправьте новое фото обложки альбома:",
        reply_markup=photo_upload_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(VinylStates.waiting_for_edit_photo, F.photo)
async def process_edit_photo(message: Message, state: FSMContext, bot: Bot):
    """Обработать новое фото"""
    photo = message.photo[-1]

    # Получаем данные о текущем виниле для удаления старого фото
    data = await state.get_data()
    vinyl_id = data.get('vinyl_id')

    # Получаем старое фото для удаления из S3
    old_photo_url = None
    if vinyl_id:
        try:
            async with get_db_session() as db:
                service = VinylService(db)
                vinyl = await service.get_vinyl_by_id(vinyl_id)
                if vinyl and hasattr(vinyl, 'photo_url'):
                    old_photo_url = vinyl.photo_url
        except Exception as e:
            logger.error(f"Ошибка при получении старого фото: {e}")

    # Загружаем новое фото в S3
    s3_service = S3Service()
    photo_url = await s3_service.upload_photo(bot, photo, "vinyl")

    if photo_url:
        # Удаляем старое фото из S3
        if old_photo_url:
            await s3_service.delete_photo(old_photo_url)

        await message.answer("📸 Фото успешно обновлено!")
        await update_vinyl_field(message, state, photo_url=photo_url)
    else:
        await message.answer("⚠️ Не удалось загрузить новое фото.")
        await update_vinyl_field(message, state)


@router.callback_query(F.data == "skip_photo", VinylStates.waiting_for_edit_photo)
async def skip_edit_photo(callback: CallbackQuery, state: FSMContext):
    """Пропустить редактирование фото (удалить текущее)"""
    # Получаем данные о текущем виниле для удаления фото
    data = await state.get_data()
    vinyl_id = data.get('vinyl_id')

    # Получаем старое фото для удаления из S3
    if vinyl_id:
        try:
            async with get_db_session() as db:
                service = VinylService(db)
                vinyl = await service.get_vinyl_by_id(vinyl_id)
                if vinyl and hasattr(vinyl, 'photo_url') and vinyl.photo_url:
                    s3_service = S3Service()
                    await s3_service.delete_photo(vinyl.photo_url)
        except Exception as e:
            logger.error(f"Ошибка при удалении старого фото: {e}")

    await update_vinyl_field(callback.message, state, photo_url=None)
    await callback.answer("Фото удалено")


async def update_vinyl_field(message: Message, state: FSMContext, **kwargs):
    """Обновить поле винила"""
    data = await state.get_data()
    vinyl_id = data.get('vinyl_id')

    if not vinyl_id:
        await message.edit_text(
            "❌ Ошибка: винил не выбран",
            reply_markup=vinyl_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        return

    try:
        async with get_db_session() as db:
            service = VinylService(db)
            vinyl = await service.update_vinyl(vinyl_id, **kwargs)

            if vinyl:
                await service.commit()
                info = await service.format_vinyl_info(vinyl)
                # Безопасное редактирование сообщения
                try:
                    await message.edit_text(
                        f"✅ *Винил обновлен!*\n\n{info}",
                        reply_markup=vinyl_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                except Exception as edit_error:
                    logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
                    await message.answer(
                        f"✅ *Винил обновлен!*\n\n{info}",
                        reply_markup=vinyl_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                logger.info(f"Обновлен винил с ID: {vinyl_id}")
            else:
                # Безопасное редактирование сообщения об ошибке
                try:
                    await message.edit_text(
                        "❌ Винил не найден",
                        reply_markup=vinyl_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                except Exception as edit_error:
                    logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
                    await message.answer(
                        "❌ Винил не найден",
                        reply_markup=vinyl_menu_keyboard(),
                        parse_mode="Markdown"
                    )

    except Exception as e:
        logger.error(f"Ошибка при обновлении винила: {e}")
        # Безопасное редактирование сообщения об ошибке
        try:
            await message.edit_text(
                "❌ Произошла ошибка при обновлении винила",
                reply_markup=vinyl_menu_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Произошла ошибка при обновлении винила",
                reply_markup=vinyl_menu_keyboard(),
                parse_mode="Markdown"
            )

    await state.clear()


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
