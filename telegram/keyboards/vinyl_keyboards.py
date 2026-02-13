"""
Клавиатуры для управления винилом
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def vinyl_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления винилом"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список винила", callback_data="vinyl_list"),
        InlineKeyboardButton(text="➕ Добавить винил", callback_data="vinyl_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="vinyl_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="vinyl_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="vinyl_search"),
        InlineKeyboardButton(text="🎭 По жанрам", callback_data="vinyl_by_genre"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1, 1, 2, 2, 1)
    return builder.as_markup()


def vinyl_selection_keyboard(vinyl_records: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора винила"""
    builder = InlineKeyboardBuilder()

    for vinyl in vinyl_records:
        display_text = f"{vinyl['artist']} - {vinyl['title']}"
        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_vinyl_{vinyl['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="vinyl_menu"))
    builder.adjust(1)
    return builder.as_markup()


def genres_selection_keyboard(genres: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура выбора жанров"""
    builder = InlineKeyboardBuilder()

    for genre in genres:
        builder.add(
            InlineKeyboardButton(
                text=genre,
                callback_data=f"select_genre_{genre}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="vinyl_menu"))
    builder.adjust(2)
    return builder.as_markup()


def vinyl_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования винила"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🎤 Исполнитель", callback_data="edit_vinyl_artist"),
        InlineKeyboardButton(text="🎵 Название", callback_data="edit_vinyl_title"),
        InlineKeyboardButton(text="📅 Год", callback_data="edit_vinyl_year"),
        InlineKeyboardButton(text="🎭 Жанры", callback_data="edit_vinyl_genres"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="vinyl_menu")
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def year_selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора года (последние 50 лет)"""
    builder = InlineKeyboardBuilder()

    import datetime
    current_year = datetime.datetime.now().year

    # Добавляем годы от текущего до 50 лет назад
    years = list(range(current_year, current_year - 50, -1))

    for year in years[:20]:  # Показываем только первые 20 лет
        builder.add(
            InlineKeyboardButton(
                text=str(year),
                callback_data=f"select_year_{year}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="✏️ Ввести вручную", callback_data="manual_year"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(4, 4, 4, 4, 4, 3)
    return builder.as_markup()


def popular_genres_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных жанров"""
    builder = InlineKeyboardBuilder()

    popular_genres = [
        "Rock", "Pop", "Jazz", "Classical",
        "Electronic", "Hip-Hop", "Blues", "Folk",
        "Metal", "Punk", "Reggae", "Country"
    ]

    for genre in popular_genres:
        builder.add(
            InlineKeyboardButton(
                text=genre,
                callback_data=f"add_genre_{genre}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✅ Готово", callback_data="genres_done"),
        InlineKeyboardButton(text="✏️ Свой жанр", callback_data="custom_genre"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(3, 3, 3, 3, 3)
    return builder.as_markup()


def confirm_delete_keyboard(vinyl_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления винила"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_vinyl_{vinyl_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="vinyl_menu")
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


def back_to_vinyl_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню винила"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К винилу", callback_data="vinyl_menu"))
    return builder.as_markup()
