"""
Клавиатуры для управления фигурками
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def figures_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления фигурками"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список фигурок", callback_data="figures_list"),
        InlineKeyboardButton(text="➕ Добавить фигурку", callback_data="figures_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="figures_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="figures_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="figures_search"),
        InlineKeyboardButton(text="🏷️ По брендам", callback_data="figures_by_brand"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1, 1, 2, 2, 1)
    return builder.as_markup()


def figures_selection_keyboard(figures: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора фигурки"""
    builder = InlineKeyboardBuilder()

    for figure in figures:
        display_text = f"{figure['name']} ({figure['brand']})"
        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_figure_{figure['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="figures_menu"))
    builder.adjust(1)
    return builder.as_markup()


def figure_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования фигурки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🎭 Название", callback_data="edit_figure_name"),
        InlineKeyboardButton(text="🏷️ Бренд", callback_data="edit_figure_brand"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="figures_menu")
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def popular_figure_brands_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных брендов фигурок"""
    builder = InlineKeyboardBuilder()

    popular_brands = [
        "Funko Pop", "Nendoroid", "figma", "Hot Toys",
        "Banpresto", "Kotobukiya", "Medicom", "McFarlane",
        "NECA", "Hasbro", "Mattel", "Jakks Pacific"
    ]

    for brand in popular_brands:
        builder.add(
            InlineKeyboardButton(
                text=brand,
                callback_data=f"select_figure_brand_{brand}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Свой бренд", callback_data="custom_figure_brand"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(3, 3, 3, 3, 2)
    return builder.as_markup()


def brands_filter_keyboard(brands: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по брендам"""
    builder = InlineKeyboardBuilder()

    for brand in brands:
        builder.add(
            InlineKeyboardButton(
                text=brand,
                callback_data=f"filter_brand_{brand}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="figures_menu"))
    builder.adjust(2)
    return builder.as_markup()


def confirm_delete_figure_keyboard(figure_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления фигурки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_figure_{figure_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="figures_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def cancel_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура отмены"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action"))
    return builder.as_markup()


def back_to_figures_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню фигурок"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К фигуркам", callback_data="figures_menu"))
    return builder.as_markup()
