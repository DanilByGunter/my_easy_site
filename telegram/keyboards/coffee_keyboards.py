"""
Клавиатуры для управления кофе
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="☕ Управление кофе"),
        KeyboardButton(text="📊 Статистика"),
        KeyboardButton(text="❓ Помощь")
    )
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def coffee_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления кофе"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🏷️ Бренды", callback_data="coffee_brands"),
        InlineKeyboardButton(text="☕ Кофе", callback_data="coffee_list"),
        InlineKeyboardButton(text="📝 Отзывы", callback_data="coffee_reviews"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def coffee_brands_keyboard() -> InlineKeyboardMarkup:
    """Меню управления брендами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список брендов", callback_data="brands_list"),
        InlineKeyboardButton(text="➕ Добавить бренд", callback_data="brand_add"),
        InlineKeyboardButton(text="✏️ Редактировать бренд", callback_data="brand_edit"),
        InlineKeyboardButton(text="🗑️ Удалить бренд", callback_data="brand_delete"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="coffee_menu")
    )
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup()


def coffee_list_keyboard() -> InlineKeyboardMarkup:
    """Меню управления кофе"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список кофе", callback_data="coffee_show_list"),
        InlineKeyboardButton(text="➕ Добавить кофе", callback_data="coffee_add"),
        InlineKeyboardButton(text="✏️ Редактировать кофе", callback_data="coffee_edit"),
        InlineKeyboardButton(text="🗑️ Удалить кофе", callback_data="coffee_delete"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="coffee_menu")
    )
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup()


def coffee_reviews_keyboard() -> InlineKeyboardMarkup:
    """Меню управления отзывами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список отзывов", callback_data="reviews_list"),
        InlineKeyboardButton(text="➕ Добавить отзыв", callback_data="review_add"),
        InlineKeyboardButton(text="✏️ Редактировать отзыв", callback_data="review_edit"),
        InlineKeyboardButton(text="🗑️ Удалить отзыв", callback_data="review_delete"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="coffee_menu")
    )
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup()


def brands_selection_keyboard(brands: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора бренда"""
    builder = InlineKeyboardBuilder()

    for brand in brands:
        builder.add(
            InlineKeyboardButton(
                text=brand['name'],
                callback_data=f"select_brand_{brand['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="coffee_menu"))
    builder.adjust(1)
    return builder.as_markup()


def coffee_selection_keyboard(coffees: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора кофе"""
    builder = InlineKeyboardBuilder()

    for coffee in coffees:
        builder.add(
            InlineKeyboardButton(
                text=f"{coffee['name']} ({coffee.get('brand_name', 'Неизвестный бренд')})",
                callback_data=f"select_coffee_{coffee['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="coffee_menu"))
    builder.adjust(1)
    return builder.as_markup()


def confirm_keyboard(action: str, item_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения действия"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_{action}_{item_id}"),
        InlineKeyboardButton(text="❌ Нет", callback_data="cancel_action"),
    )
    builder.adjust(2)
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


def rating_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора рейтинга"""
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки с рейтингами от 1 до 10
    for i in range(1, 11):
        builder.add(InlineKeyboardButton(text=str(i), callback_data=f"rating_{i}"))

    builder.add(
        InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_field"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(5, 5, 2)  # 5 кнопок в первых двух рядах, 2 в последнем
    return builder.as_markup()


def brewing_methods_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора способа приготовления"""
    builder = InlineKeyboardBuilder()

    methods = [
        ("☕ Эспрессо", "espresso"),
        ("🥛 Капучино", "cappuccino"),
        ("🤍 Латте", "latte"),
        ("⚫ Американо", "americano"),
        ("🔥 Турка", "turka"),
        ("💧 Фильтр", "filter"),
        ("🌊 Пуровер", "pourover"),
        ("🫖 Френч-пресс", "french_press"),
        ("❄️ Колд брю", "cold_brew"),
        ("✏️ Другой", "other")
    ]

    for text, callback in methods:
        builder.add(InlineKeyboardButton(text=text, callback_data=f"method_{callback}"))

    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action"))
    builder.adjust(2, 2, 2, 2, 2, 1)
    return builder.as_markup()
