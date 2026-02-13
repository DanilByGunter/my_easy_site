"""
Клавиатуры для управления растениями
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def plants_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления растениями"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список растений", callback_data="plants_list"),
        InlineKeyboardButton(text="➕ Добавить растение", callback_data="plants_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="plants_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="plants_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="plants_search"),
        InlineKeyboardButton(text="👨‍👩‍👧‍👦 По семействам", callback_data="plants_by_family"),
        InlineKeyboardButton(text="🧬 По родам", callback_data="plants_by_genus"),
        InlineKeyboardButton(text="📸 Фотографии", callback_data="plants_photos"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1, 1, 2, 2, 2, 1, 1)
    return builder.as_markup()


def plants_selection_keyboard(plants: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора растения"""
    builder = InlineKeyboardBuilder()

    for plant in plants:
        # Формируем отображаемое название
        display_parts = []
        if plant.get('common_name'):
            display_parts.append(plant['common_name'])
        if plant.get('genus') and plant.get('species'):
            display_parts.append(f"({plant['genus']} {plant['species']})")
        elif plant.get('genus'):
            display_parts.append(f"({plant['genus']})")

        display_text = " ".join(display_parts) if display_parts else "Растение без названия"

        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_plant_{plant['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="plants_menu"))
    builder.adjust(1)
    return builder.as_markup()


def plant_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования растения"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🏷️ Название", callback_data="edit_plant_common_name"),
        InlineKeyboardButton(text="👨‍👩‍👧‍👦 Семейство", callback_data="edit_plant_family"),
        InlineKeyboardButton(text="🧬 Род", callback_data="edit_plant_genus"),
        InlineKeyboardButton(text="🔬 Вид", callback_data="edit_plant_species"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="plants_menu")
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def popular_plant_families_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных семейств растений"""
    builder = InlineKeyboardBuilder()

    popular_families = [
        "Rosaceae", "Asteraceae", "Fabaceae", "Poaceae",
        "Lamiaceae", "Solanaceae", "Brassicaceae", "Apiaceae",
        "Euphorbiaceae", "Rubiaceae", "Malvaceae", "Orchidaceae",
        "Cactaceae", "Araceae", "Arecaceae", "Liliaceae"
    ]

    for family in popular_families:
        builder.add(
            InlineKeyboardButton(
                text=family,
                callback_data=f"select_plant_family_{family}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Свое семейство", callback_data="custom_plant_family"),
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(4, 4, 4, 4, 3)
    return builder.as_markup()


def families_filter_keyboard(families: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по семействам"""
    builder = InlineKeyboardBuilder()

    for family in families:
        builder.add(
            InlineKeyboardButton(
                text=family,
                callback_data=f"filter_family_{family}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="plants_menu"))
    builder.adjust(2)
    return builder.as_markup()


def genera_filter_keyboard(genera: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по родам"""
    builder = InlineKeyboardBuilder()

    for genus in genera:
        builder.add(
            InlineKeyboardButton(
                text=genus,
                callback_data=f"filter_genus_{genus}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="plants_menu"))
    builder.adjust(2)
    return builder.as_markup()


def photos_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления фотографиями растений"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Все фото", callback_data="photos_list"),
        InlineKeyboardButton(text="➕ Добавить фото", callback_data="photos_add"),
        InlineKeyboardButton(text="🌱 Растения с фото", callback_data="plants_with_photos"),
        InlineKeyboardButton(text="🔙 К растениям", callback_data="plants_menu")
    )
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def date_format_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора формата даты"""
    builder = InlineKeyboardBuilder()

    import datetime
    today = datetime.date.today()

    builder.add(
        InlineKeyboardButton(text="📅 Сегодня", callback_data=f"select_date_{today.isoformat()}"),
        InlineKeyboardButton(text="📅 Вчера", callback_data=f"select_date_{(today - datetime.timedelta(days=1)).isoformat()}"),
        InlineKeyboardButton(text="✏️ Ввести дату", callback_data="manual_date"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(2, 2)
    return builder.as_markup()


def confirm_delete_plant_keyboard(plant_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления растения"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_plant_{plant_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="plants_menu")
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


def back_to_plants_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню растений"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К растениям", callback_data="plants_menu"))
    return builder.as_markup()
