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


def dynamic_genres_keyboard(existing_genres=None) -> InlineKeyboardMarkup:
    """Клавиатура жанров из БД + популярные"""
    builder = InlineKeyboardBuilder()

    # Популярные жанры как fallback
    popular_genres = [
        "Фантастика", "Фэнтези", "Детектив", "Роман",
        "Классика", "Биография", "История", "Философия",
        "Психология", "Бизнес", "Научпоп", "Поэзия"
    ]

    # Используем жанры из БД, если есть, иначе популярные
    genres_to_show = existing_genres if existing_genres else popular_genres

    for genre in genres_to_show[:12]:  # Показываем максимум 12
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
    builder.adjust(3, 3, 3, 3, 3)
    return builder.as_markup()


def dynamic_languages_keyboard(existing_languages=None) -> InlineKeyboardMarkup:
    """Клавиатура языков из БД + популярные"""
    builder = InlineKeyboardBuilder()

    # Популярные языки как fallback
    popular_languages = [
        "Русский", "English", "Español", "Français",
        "Deutsch", "Italiano", "中文", "日本語"
    ]

    # Используем языки из БД, если есть, иначе популярные
    languages_to_show = existing_languages if existing_languages else popular_languages

    for language in languages_to_show[:12]:  # Показываем максимум 12
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


def dynamic_formats_keyboard(existing_formats=None) -> InlineKeyboardMarkup:
    """Клавиатура форматов из БД + популярные"""
    builder = InlineKeyboardBuilder()

    # Популярные форматы как fallback
    popular_formats = [
        "Бумажная", "Электронная", "Аудиокнига",
        "PDF", "EPUB", "FB2", "MOBI"
    ]

    # Используем форматы из БД, если есть, иначе популярные
    formats_to_show = existing_formats if existing_formats else popular_formats

    for format_type in formats_to_show[:12]:  # Показываем максимум 12
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


# Оставляем старые функции для совместимости
def popular_genres_books_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных жанров книг"""
    return dynamic_genres_keyboard()


def languages_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языков"""
    return dynamic_languages_keyboard()


def book_formats_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора форматов книг"""
    return dynamic_formats_keyboard()


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
