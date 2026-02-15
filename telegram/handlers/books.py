"""
Обработчики для управления книгами
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import get_db_session
from services.books_service import BooksService
from states.books_states import BooksStates
from keyboards.books_keyboards import (
    books_menu_keyboard, books_selection_keyboard, book_edit_fields_keyboard,
    dynamic_genres_keyboard, dynamic_languages_keyboard, dynamic_formats_keyboard,
    confirm_delete_book_keyboard, cancel_keyboard, skip_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


# === ОСНОВНОЕ МЕНЮ ===

@router.callback_query(F.data == "books_list")
async def show_books_list(callback: CallbackQuery):
    """Показать список всех книг"""
    async with get_db_session() as db:
        service = BooksService(db)
        books = await service.get_all_books()

    if not books:
        text = "📋 *Список книг*\n\n❌ Книги не найдены"
    else:
        text = "📋 *Список книг:*\n\n"
        for i, book in enumerate(books, 1):
            text += f"{i}. *{book.title}*"
            if book.author:
                text += f" - {book.author}"
            if book.genre:
                text += f"\n   🎭 {book.genre}"
            if book.language:
                text += f" | 🌐 {book.language}"
            text += "\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=books_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "books_add")
async def start_add_book(callback: CallbackQuery, state: FSMContext):
    """Начать добавление новой книги"""
    await state.set_state(BooksStates.waiting_for_title)

    await callback.message.edit_text(
        "➕ *Добавление новой книги*\n\n"
        "Введите название книги:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Обработать название книги"""
    title = message.text.strip()

    if not title:
        await message.answer(
            "❌ Название книги не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(title=title)
    await state.set_state(BooksStates.waiting_for_author)

    await message.answer(
        "✍️ *Автор книги*\n\n"
        "Введите автора книги:",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )


@router.message(BooksStates.waiting_for_author)
async def process_author(message: Message, state: FSMContext):
    """Обработать автора книги"""
    author = message.text.strip()

    if not author:
        await message.answer(
            "❌ Имя автора не может быть пустым. Попробуйте еще раз или пропустите:",
            reply_markup=skip_keyboard()
        )
        return

    await state.update_data(author=author)
    await state.set_state(BooksStates.waiting_for_genre)

    # Получаем существующие жанры из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_genres = await service.get_all_genres()

    await message.answer(
        "🎭 *Жанр книги*\n\n"
        "Выберите жанр книги:",
        reply_markup=dynamic_genres_keyboard(existing_genres),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("select_book_genre_"))
async def process_genre_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор жанра"""
    genre = callback.data.split("_")[-1]

    await state.update_data(genre=genre)
    await state.set_state(BooksStates.waiting_for_language)

    # Получаем существующие языки из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_languages = await service.get_all_languages()

    await callback.message.edit_text(
        "🌐 *Язык книги*\n\n"
        "Выберите язык книги:",
        reply_markup=dynamic_languages_keyboard(existing_languages),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_language_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор языка"""
    language = callback.data.split("_")[-1]

    await state.update_data(language=language)
    await state.set_state(BooksStates.waiting_for_format)

    # Получаем существующие форматы из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_formats = await service.get_all_formats()

    await callback.message.edit_text(
        "📚 *Формат книги*\n\n"
        "Выберите формат книги:",
        reply_markup=dynamic_formats_keyboard(existing_formats),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_format_"))
async def process_format_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор формата"""
    format_type = callback.data.split("_")[-1]

    await state.update_data(format=format_type)
    await state.set_state(BooksStates.waiting_for_review)

    await callback.message.edit_text(
        "📝 *Рецензия*\n\n"
        "Напишите рецензию на книгу или пропустите:",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_review)
async def process_review(message: Message, state: FSMContext):
    """Обработать рецензию"""
    review = message.text.strip()

    await state.update_data(review=review)
    await state.set_state(BooksStates.waiting_for_opinion)

    await message.answer(
        "💭 *Личное мнение*\n\n"
        "Напишите ваше мнение о книге или пропустите:",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )


@router.message(BooksStates.waiting_for_opinion)
async def process_opinion(message: Message, state: FSMContext):
    """Обработать мнение"""
    opinion = message.text.strip()

    await state.update_data(opinion=opinion)
    await finish_adding_book_with_data(message, state)


@router.callback_query(F.data == "skip_field")
async def skip_field(callback: CallbackQuery, state: FSMContext):
    """Пропустить поле"""
    current_state = await state.get_state()

    if current_state == BooksStates.waiting_for_author.state:
        await state.update_data(author=None)
        await state.set_state(BooksStates.waiting_for_genre)

        # Получаем существующие жанры из БД
        async with get_db_session() as db:
            service = BooksService(db)
            existing_genres = await service.get_all_genres()

        await callback.message.edit_text(
            "🎭 *Жанр книги*\n\n"
            "Выберите жанр книги:",
            reply_markup=dynamic_genres_keyboard(existing_genres),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_genre.state:
        await state.update_data(genre=None)
        await state.set_state(BooksStates.waiting_for_language)

        # Получаем существующие языки из БД
        async with get_db_session() as db:
            service = BooksService(db)
            existing_languages = await service.get_all_languages()

        await callback.message.edit_text(
            "🌐 *Язык книги*\n\n"
            "Выберите язык книги:",
            reply_markup=dynamic_languages_keyboard(existing_languages),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_language.state:
        await state.update_data(language=None)
        await state.set_state(BooksStates.waiting_for_format)

        # Получаем существующие форматы из БД
        async with get_db_session() as db:
            service = BooksService(db)
            existing_formats = await service.get_all_formats()

        await callback.message.edit_text(
            "📚 *Формат книги*\n\n"
            "Выберите формат книги:",
            reply_markup=dynamic_formats_keyboard(existing_formats),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_format.state:
        await state.update_data(format=None)
        await state.set_state(BooksStates.waiting_for_review)

        await callback.message.edit_text(
            "📝 *Рецензия*\n\n"
            "Напишите рецензию на книгу или пропустите:",
            reply_markup=skip_keyboard(),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_review.state:
        await state.update_data(review=None)
        await state.set_state(BooksStates.waiting_for_opinion)

        await callback.message.edit_text(
            "💭 *Личное мнение*\n\n"
            "Напишите ваше мнение о книге или пропустите:",
            reply_markup=skip_keyboard(),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_opinion.state:
        await state.update_data(opinion=None)
        await finish_adding_book_with_data(callback.message, state)

    await callback.answer("Поле пропущено")


async def finish_adding_book_with_data(message: Message, state: FSMContext):
    """Завершить добавление книги с данными"""
    data = await state.get_data()

    # Проверяем наличие обязательных полей
    if not data.get('title'):
        logger.error(f"Отсутствуют обязательные данные для создания книги: {data}")
        try:
            await message.edit_text(
                "❌ Ошибка: отсутствует название книги.",
                reply_markup=books_menu_keyboard()
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Ошибка: отсутствует название книги.",
                reply_markup=books_menu_keyboard()
            )
        await state.clear()
        return

    try:
        async with get_db_session() as db:
            service = BooksService(db)
            book = await service.create_book(
                title=data['title'],
                author=data.get('author'),
                genre=data.get('genre'),
                language=data.get('language'),
                format=data.get('format'),
                review=data.get('review'),
                opinion=data.get('opinion')
            )
            await service.commit()

            # Форматируем информацию о созданной книге
            info = "✅ *Книга добавлена!*\n\n"
            info += await service.format_book_info(book)

        await state.clear()

        # Безопасное редактирование сообщения
        try:
            await message.edit_text(
                info,
                reply_markup=books_menu_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as edit_error:
            # Если не удалось отредактировать, отправляем новое сообщение
            logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
            await message.answer(
                info,
                reply_markup=books_menu_keyboard(),
                parse_mode="Markdown"
            )

        logger.info(f"Добавлена новая книга: {book.title}")

    except Exception as e:
        logger.error(f"Ошибка при добавлении книги: {e}")
        # Безопасное редактирование сообщения об ошибке
        try:
            await message.edit_text(
                "❌ Произошла ошибка при добавлении книги.",
                reply_markup=books_menu_keyboard()
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Произошла ошибка при добавлении книги.",
                reply_markup=books_menu_keyboard()
            )
        await state.clear()


# === УДАЛЕНИЕ КНИГИ ===

@router.callback_query(F.data == "books_delete")
async def start_delete_book(callback: CallbackQuery, state: FSMContext):
    """Начать удаление книги"""
    async with get_db_session() as db:
        service = BooksService(db)
        books = await service.get_all_books()

    if not books:
        await callback.message.edit_text(
            "🗑️ *Удаление книги*\n\n❌ Книги не найдены",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    await state.set_state(BooksStates.waiting_for_delete_selection)

    await callback.message.edit_text(
        "🗑️ *Удаление книги*\n\n"
        "Выберите книгу для удаления:",
        reply_markup=books_selection_keyboard(books),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_book_"), BooksStates.waiting_for_delete_selection)
async def confirm_delete_book(callback: CallbackQuery, state: FSMContext):
    """Подтвердить удаление книги"""
    book_id = callback.data.split("_")[-1]

    async with get_db_session() as db:
        service = BooksService(db)
        book = await service.get_book_by_id(book_id)

    if not book:
        await callback.message.edit_text(
            "❌ Книга не найдена",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return

    await state.update_data(book_id=book_id)
    await state.set_state(BooksStates.waiting_for_delete_confirmation)

    info = await BooksService(None).format_book_info(book)
    await callback.message.edit_text(
        f"🗑️ *Удаление книги*\n\n"
        f"{info}\n"
        f"❓ Вы уверены, что хотите удалить эту книгу?",
        reply_markup=confirm_delete_book_keyboard(book_id),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_book_"))
async def delete_book_confirmed(callback: CallbackQuery, state: FSMContext):
    """Удалить книгу после подтверждения"""
    book_id = callback.data.split("_")[-1]

    try:
        async with get_db_session() as db:
            service = BooksService(db)
            success = await service.delete_book(book_id)

            if success:
                await service.commit()
                await callback.message.edit_text(
                    "✅ *Книга успешно удалена!*",
                    reply_markup=books_menu_keyboard(),
                    parse_mode="Markdown"
                )
                logger.info(f"Удалена книга с ID: {book_id}")
            else:
                await callback.message.edit_text(
                    "❌ Книга не найдена или уже удалена",
                    reply_markup=books_menu_keyboard(),
                    parse_mode="Markdown"
                )

    except Exception as e:
        logger.error(f"Ошибка при удалении книги: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при удалении книги",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )

    await state.clear()
    await callback.answer()


# === РЕДАКТИРОВАНИЕ КНИГИ ===

@router.callback_query(F.data == "books_edit")
async def start_edit_book(callback: CallbackQuery, state: FSMContext):
    """Начать редактирование книги"""
    async with get_db_session() as db:
        service = BooksService(db)
        books = await service.get_all_books()

    if not books:
        await callback.message.edit_text(
            "✏️ *Редактирование книги*\n\n❌ Книги не найдены",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    await state.set_state(BooksStates.waiting_for_book_selection)

    await callback.message.edit_text(
        "✏️ *Редактирование книги*\n\n"
        "Выберите книгу для редактирования:",
        reply_markup=books_selection_keyboard(books),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_book_"), BooksStates.waiting_for_book_selection)
async def select_edit_field(callback: CallbackQuery, state: FSMContext):
    """Выбрать поле для редактирования"""
    book_id = callback.data.split("_")[-1]

    async with get_db_session() as db:
        service = BooksService(db)
        book = await service.get_book_by_id(book_id)

    if not book:
        await callback.message.edit_text(
            "❌ Книга не найдена",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return

    await state.update_data(book_id=book_id)
    await state.set_state(BooksStates.waiting_for_edit_field_selection)

    info = await BooksService(None).format_book_info(book)
    await callback.message.edit_text(
        f"✏️ *Редактирование книги*\n\n"
        f"{info}\n"
        f"Выберите поле для редактирования:",
        reply_markup=book_edit_fields_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


# === ОБРАБОТЧИКИ РЕДАКТИРОВАНИЯ ПОЛЕЙ ===

@router.callback_query(F.data == "edit_book_title")
async def edit_title(callback: CallbackQuery, state: FSMContext):
    """Редактировать название"""
    await state.set_state(BooksStates.waiting_for_edit_title)

    await callback.message.edit_text(
        "📖 *Редактирование названия*\n\n"
        "Введите новое название книги:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_edit_title)
async def process_edit_title(message: Message, state: FSMContext):
    """Обработать новое название"""
    title = message.text.strip()

    if not title:
        await message.answer(
            "❌ Название книги не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await update_book_field(message, state, title=title)


@router.callback_query(F.data == "edit_book_author")
async def edit_author(callback: CallbackQuery, state: FSMContext):
    """Редактировать автора"""
    await state.set_state(BooksStates.waiting_for_edit_author)

    await callback.message.edit_text(
        "✍️ *Редактирование автора*\n\n"
        "Введите нового автора:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_edit_author)
async def process_edit_author(message: Message, state: FSMContext):
    """Обработать нового автора"""
    author = message.text.strip()

    if not author:
        await message.answer(
            "❌ Имя автора не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await update_book_field(message, state, author=author)


@router.callback_query(F.data == "edit_book_genre")
async def edit_genre(callback: CallbackQuery, state: FSMContext):
    """Редактировать жанр"""
    await state.set_state(BooksStates.waiting_for_edit_genre)

    # Получаем существующие жанры из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_genres = await service.get_all_genres()

    await callback.message.edit_text(
        "🎭 *Редактирование жанра*\n\n"
        "Выберите новый жанр:",
        reply_markup=dynamic_genres_keyboard(existing_genres),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_book_genre_"), BooksStates.waiting_for_edit_genre)
async def process_edit_genre_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор жанра при редактировании"""
    genre = callback.data.split("_")[-1]
    await update_book_field(callback.message, state, genre=genre)
    await callback.answer()


@router.callback_query(F.data == "edit_book_language")
async def edit_language(callback: CallbackQuery, state: FSMContext):
    """Редактировать язык"""
    await state.set_state(BooksStates.waiting_for_edit_language)

    # Получаем существующие языки из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_languages = await service.get_all_languages()

    await callback.message.edit_text(
        "🌐 *Редактирование языка*\n\n"
        "Выберите новый язык:",
        reply_markup=dynamic_languages_keyboard(existing_languages),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_language_"), BooksStates.waiting_for_edit_language)
async def process_edit_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор языка при редактировании"""
    language = callback.data.split("_")[-1]
    await update_book_field(callback.message, state, language=language)
    await callback.answer()


@router.callback_query(F.data == "edit_book_format")
async def edit_format(callback: CallbackQuery, state: FSMContext):
    """Редактировать формат"""
    await state.set_state(BooksStates.waiting_for_edit_format)

    # Получаем существующие форматы из БД
    async with get_db_session() as db:
        service = BooksService(db)
        existing_formats = await service.get_all_formats()

    await callback.message.edit_text(
        "📚 *Редактирование формата*\n\n"
        "Выберите новый формат:",
        reply_markup=dynamic_formats_keyboard(existing_formats),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_format_"), BooksStates.waiting_for_edit_format)
async def process_edit_format_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор формата при редактировании"""
    format_type = callback.data.split("_")[-1]
    await update_book_field(callback.message, state, format=format_type)
    await callback.answer()


@router.callback_query(F.data == "edit_book_review")
async def edit_review(callback: CallbackQuery, state: FSMContext):
    """Редактировать рецензию"""
    await state.set_state(BooksStates.waiting_for_edit_review)

    await callback.message.edit_text(
        "📝 *Редактирование рецензии*\n\n"
        "Введите новую рецензию:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_edit_review)
async def process_edit_review(message: Message, state: FSMContext):
    """Обработать новую рецензию"""
    review = message.text.strip()
    await update_book_field(message, state, review=review)


@router.callback_query(F.data == "edit_book_opinion")
async def edit_opinion(callback: CallbackQuery, state: FSMContext):
    """Редактировать мнение"""
    await state.set_state(BooksStates.waiting_for_edit_opinion)

    await callback.message.edit_text(
        "💭 *Редактирование мнения*\n\n"
        "Введите новое мнение:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(BooksStates.waiting_for_edit_opinion)
async def process_edit_opinion(message: Message, state: FSMContext):
    """Обработать новое мнение"""
    opinion = message.text.strip()
    await update_book_field(message, state, opinion=opinion)


# === ОБРАБОТЧИКИ ПОЛЬЗОВАТЕЛЬСКОГО ВВОДА ===

@router.callback_query(F.data == "custom_book_genre")
async def custom_genre_input(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод жанра"""
    current_state = await state.get_state()

    if current_state == BooksStates.waiting_for_genre.state:
        await callback.message.edit_text(
            "🎭 *Жанр книги*\n\n"
            "Введите жанр книги:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_edit_genre.state:
        await callback.message.edit_text(
            "🎭 *Редактирование жанра*\n\n"
            "Введите новый жанр:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    await callback.answer()


@router.callback_query(F.data == "custom_language")
async def custom_language_input(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод языка"""
    current_state = await state.get_state()

    if current_state == BooksStates.waiting_for_language.state:
        await callback.message.edit_text(
            "🌐 *Язык книги*\n\n"
            "Введите язык книги:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_edit_language.state:
        await callback.message.edit_text(
            "🌐 *Редактирование языка*\n\n"
            "Введите новый язык:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    await callback.answer()


@router.callback_query(F.data == "custom_format")
async def custom_format_input(callback: CallbackQuery, state: FSMContext):
    """Ручной ввод формата"""
    current_state = await state.get_state()

    if current_state == BooksStates.waiting_for_format.state:
        await callback.message.edit_text(
            "📚 *Формат книги*\n\n"
            "Введите формат книги:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    elif current_state == BooksStates.waiting_for_edit_format.state:
        await callback.message.edit_text(
            "📚 *Редактирование формата*\n\n"
            "Введите новый формат:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
    await callback.answer()


async def update_book_field(message: Message, state: FSMContext, **kwargs):
    """Обновить поле книги"""
    data = await state.get_data()
    book_id = data.get('book_id')

    if not book_id:
        await message.edit_text(
            "❌ Ошибка: книга не выбрана",
            reply_markup=books_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        return

    try:
        async with get_db_session() as db:
            service = BooksService(db)
            book = await service.update_book(book_id, **kwargs)

            if book:
                await service.commit()
                info = await service.format_book_info(book)
                # Безопасное редактирование сообщения
                try:
                    await message.edit_text(
                        f"✅ *Книга обновлена!*\n\n{info}",
                        reply_markup=books_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                except Exception as edit_error:
                    logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
                    await message.answer(
                        f"✅ *Книга обновлена!*\n\n{info}",
                        reply_markup=books_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                logger.info(f"Обновлена книга с ID: {book_id}")
            else:
                # Безопасное редактирование сообщения об ошибке
                try:
                    await message.edit_text(
                        "❌ Книга не найдена",
                        reply_markup=books_menu_keyboard(),
                        parse_mode="Markdown"
                    )
                except Exception as edit_error:
                    logger.warning(f"Не удалось отредактировать сообщение: {edit_error}")
                    await message.answer(
                        "❌ Книга не найдена",
                        reply_markup=books_menu_keyboard(),
                        parse_mode="Markdown"
                    )

    except Exception as e:
        logger.error(f"Ошибка при обновлении книги: {e}")
        # Безопасное редактирование сообщения об ошибке
        try:
            await message.edit_text(
                "❌ Произошла ошибка при обновлении книги",
                reply_markup=books_menu_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as edit_error:
            logger.warning(f"Не удалось отредактировать сообщение об ошибке: {edit_error}")
            await message.answer(
                "❌ Произошла ошибка при обновлении книги",
                reply_markup=books_menu_keyboard(),
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
        reply_markup=books_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer("Действие отменено")
