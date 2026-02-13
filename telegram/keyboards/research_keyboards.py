"""
Клавиатуры для управления исследованиями
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def research_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления исследованиями"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📄 Публикации", callback_data="publications_menu"),
        InlineKeyboardButton(text="📊 Инфографики", callback_data="infographics_menu"),
        InlineKeyboardButton(text="📈 Статистика", callback_data="research_statistics"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def publications_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления публикациями"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список публикаций", callback_data="publications_list"),
        InlineKeyboardButton(text="➕ Добавить публикацию", callback_data="publications_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="publications_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="publications_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="publications_search"),
        InlineKeyboardButton(text="📅 По годам", callback_data="publications_by_year"),
        InlineKeyboardButton(text="🏛️ По местам", callback_data="publications_by_venue"),
        InlineKeyboardButton(text="🔙 К исследованиям", callback_data="research_menu")
    )
    builder.adjust(1, 1, 2, 2, 1, 1)
    return builder.as_markup()


def infographics_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления инфографиками"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список инфографик", callback_data="infographics_list"),
        InlineKeyboardButton(text="➕ Добавить инфографику", callback_data="infographics_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="infographics_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="infographics_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="infographics_search"),
        InlineKeyboardButton(text="🏷️ По темам", callback_data="infographics_by_topic"),
        InlineKeyboardButton(text="🔙 К исследованиям", callback_data="research_menu")
    )
    builder.adjust(1, 1, 2, 2, 1)
    return builder.as_markup()


def publications_selection_keyboard(publications: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора публикации"""
    builder = InlineKeyboardBuilder()

    for pub in publications:
        display_text = pub['title']
        if pub.get('year'):
            display_text += f" ({pub['year']})"

        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_publication_{pub['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="publications_menu"))
    builder.adjust(1)
    return builder.as_markup()


def infographics_selection_keyboard(infographics: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора инфографики"""
    builder = InlineKeyboardBuilder()

    for info in infographics:
        display_text = info['title']
        if info.get('topic'):
            display_text += f" ({info['topic']})"

        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_infographic_{info['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="infographics_menu"))
    builder.adjust(1)
    return builder.as_markup()


def publication_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования публикации"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📄 Название", callback_data="edit_publication_title"),
        InlineKeyboardButton(text="🏛️ Место", callback_data="edit_publication_venue"),
        InlineKeyboardButton(text="📅 Год", callback_data="edit_publication_year"),
        InlineKeyboardButton(text="🔗 Ссылка", callback_data="edit_publication_url"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="publications_menu")
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def infographic_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования инфографики"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📊 Название", callback_data="edit_infographic_title"),
        InlineKeyboardButton(text="🏷️ Тема", callback_data="edit_infographic_topic"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="infographics_menu")
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def years_selection_keyboard(years: List[int]) -> InlineKeyboardMarkup:
    """Клавиатура выбора года"""
    builder = InlineKeyboardBuilder()

    for year in years:
        builder.add(
            InlineKeyboardButton(
                text=str(year),
                callback_data=f"select_pub_year_{year}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Другой год", callback_data="custom_year"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(4, 3)
    return builder.as_markup()


def years_filter_keyboard(years: List[int]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по годам"""
    builder = InlineKeyboardBuilder()

    for year in years:
        builder.add(
            InlineKeyboardButton(
                text=str(year),
                callback_data=f"filter_year_{year}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="publications_menu"))
    builder.adjust(4)
    return builder.as_markup()


def venues_filter_keyboard(venues: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по местам публикации"""
    builder = InlineKeyboardBuilder()

    for venue in venues:
        display_venue = venue
        if len(display_venue) > 30:
            display_venue = display_venue[:27] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_venue,
                callback_data=f"filter_venue_{venue}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="publications_menu"))
    builder.adjust(1)
    return builder.as_markup()


def topics_filter_keyboard(topics: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по темам инфографик"""
    builder = InlineKeyboardBuilder()

    for topic in topics:
        builder.add(
            InlineKeyboardButton(
                text=topic,
                callback_data=f"filter_topic_{topic}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="infographics_menu"))
    builder.adjust(2)
    return builder.as_markup()


def popular_topics_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных тем для инфографик"""
    builder = InlineKeyboardBuilder()

    popular_topics = [
        "Наука", "Технологии", "Медицина", "Экология",
        "Образование", "Психология", "Социология", "Экономика",
        "История", "География", "Биология", "Физика"
    ]

    for topic in popular_topics:
        builder.add(
            InlineKeyboardButton(
                text=topic,
                callback_data=f"select_topic_{topic}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Своя тема", callback_data="custom_topic"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(3, 3, 3, 3, 3)
    return builder.as_markup()


def confirm_delete_publication_keyboard(publication_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления публикации"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_publication_{publication_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="publications_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def confirm_delete_infographic_keyboard(infographic_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления инфографики"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_infographic_{infographic_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="infographics_menu")
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


def back_to_research_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню исследований"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К исследованиям", callback_data="research_menu"))
    return builder.as_markup()
