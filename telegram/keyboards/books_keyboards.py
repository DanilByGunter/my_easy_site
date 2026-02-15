"""
Клавиатуры для управления книгами
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def books_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления книгами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список книг", callback_data="books_list"),
        InlineKeyboardButton(text="➕ Добавить книгу", callback_data="books_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="books_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="books_delete"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup()


def books_selection_keyboard(books) -> InlineKeyboardMarkup:
    """Клавиатура выбора книги"""
    builder = InlineKeyboardBuilder()

    for book in books:
        display_text = book.title
        if book.author:
            display_text += f" - {book.author}"

        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_book_{book.id}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="books_menu"))
    builder.adjust(1)
    return builder.as_markup()


def book_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования книги"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📖 Название", callback_data="edit_book_title"),
        InlineKeyboardButton(text="✍️ Автор", callback_data="edit_book_author"),
        InlineKeyboardButton(text="🎭 Жанр", callback_data="edit_book_genre"),
        InlineKeyboardButton(text="🌐 Язык", callback_data="edit_book_language"),
        InlineKeyboardButton(text="📚 Формат", callback_data="edit_book_format"),
        InlineKeyboardButton(text="📝 Рецензия", callback_data="edit_book_review"),
        InlineKeyboardButton(text="💭 Мнение", callback_data="edit_book_opinion"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="books_menu")
    )
    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup()


def popular_genres_books_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных жанров книг"""
    builder = InlineKeyboardBuilder()

    popular_genres = [
        "Фантастика", "Фэнтези", "Детектив", "Роман",
        "Классика", "Биография", "История", "Философия",
        "Психология", "Бизнес", "Научпоп", "Поэзия",
        "Драма", "Комедия", "Триллер", "Мистика"
    ]

    for genre in popular_genres:
        builder.add(
            InlineKeyboardButton(
                text=genre,
                callback_data=f"select_book_genre_{genre}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Свой жанр", callback_data="custom_book_genre"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(4, 4, 4, 4, 3)
    return builder.as_markup()


def languages_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языков"""
    builder = InlineKeyboardBuilder()

    languages = [
        "Русский", "English", "Español", "Français",
        "Deutsch", "Italiano", "中文", "日本語",
        "한국어", "العربية", "हिन्दी", "Português"
    ]

    for language in languages:
        builder.add(
            InlineKeyboardButton(
                text=language,
                callback_data=f"select_language_{language}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Другой язык", callback_data="custom_language"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(3, 3, 3, 3, 3)
    return builder.as_markup()


def book_formats_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора форматов книг"""
    builder = InlineKeyboardBuilder()

    formats = [
        "Бумажная", "Электронная", "Аудиокнига",
        "PDF", "EPUB", "FB2", "MOBI"
    ]

    for format_type in formats:
        builder.add(
            InlineKeyboardButton(
                text=format_type,
                callback_data=f"select_format_{format_type}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Другой формат", callback_data="custom_format"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(3, 2, 2, 3)
    return builder.as_markup()


def quotes_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления цитатами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Все цитаты", callback_data="quotes_list"),
        InlineKeyboardButton(text="➕ Добавить цитату", callback_data="quotes_add"),
        InlineKeyboardButton(text="🔙 К книгам", callback_data="books_menu")
    )
    builder.adjust(1, 1, 1)
    return builder.as_markup()


def confirm_delete_book_keyboard(book_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления книги"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_book_{book_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="books_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def cancel_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура отмены"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action"))
    return builder.as_markup()


def skip_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой пропуска"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(1)
    return builder.as_markup()


def back_to_books_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню книг"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К книгам", callback_data="books_menu"))
    return builder.as_markup()
