"""
Клавиатуры для управления проектами
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def projects_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления проектами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Список проектов", callback_data="projects_list"),
        InlineKeyboardButton(text="➕ Добавить проект", callback_data="projects_add"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="projects_edit"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data="projects_delete"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="projects_search"),
        InlineKeyboardButton(text="🏷️ По тегам", callback_data="projects_by_tag"),
        InlineKeyboardButton(text="🏷️ Управление тегами", callback_data="projects_tags_manage"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1, 1, 2, 2, 1, 1)
    return builder.as_markup()


def projects_selection_keyboard(projects: List[dict]) -> InlineKeyboardMarkup:
    """Клавиатура выбора проекта"""
    builder = InlineKeyboardBuilder()

    for project in projects:
        display_text = project['name']
        if len(display_text) > 40:
            display_text = display_text[:37] + "..."

        builder.add(
            InlineKeyboardButton(
                text=display_text,
                callback_data=f"select_project_{project['id']}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu"))
    builder.adjust(1)
    return builder.as_markup()


def project_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования проекта"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🚀 Название", callback_data="edit_project_name"),
        InlineKeyboardButton(text="📝 Описание", callback_data="edit_project_description"),
        InlineKeyboardButton(text="🏷️ Теги", callback_data="edit_project_tags"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")
    )
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def popular_project_tags_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура популярных тегов для проектов"""
    builder = InlineKeyboardBuilder()

    popular_tags = [
        "web", "mobile", "desktop", "api",
        "python", "javascript", "react", "vue",
        "django", "flask", "nodejs", "typescript",
        "ai", "ml", "data", "analytics",
        "opensource", "commercial", "personal", "study"
    ]

    for tag in popular_tags:
        builder.add(
            InlineKeyboardButton(
                text=f"#{tag}",
                callback_data=f"add_project_tag_{tag}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✅ Готово", callback_data="tags_done"),
        InlineKeyboardButton(text="✏️ Свой тег", callback_data="custom_project_tag"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )
    builder.adjust(4, 4, 4, 4, 4, 3)
    return builder.as_markup()


def tags_filter_keyboard(tags: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура фильтра по тегам"""
    builder = InlineKeyboardBuilder()

    for tag in tags:
        builder.add(
            InlineKeyboardButton(
                text=f"#{tag}",
                callback_data=f"filter_tag_{tag}"
            )
        )

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu"))
    builder.adjust(3)
    return builder.as_markup()


def tags_management_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню управления тегами"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Все теги", callback_data="tags_list"),
        InlineKeyboardButton(text="➕ Добавить тег", callback_data="tags_add_to_project"),
        InlineKeyboardButton(text="🗑️ Удалить тег", callback_data="tags_remove_from_project"),
        InlineKeyboardButton(text="📊 Статистика тегов", callback_data="tags_statistics"),
        InlineKeyboardButton(text="🔙 К проектам", callback_data="projects_menu")
    )
    builder.adjust(1, 1, 1, 1, 1)
    return builder.as_markup()


def project_tags_keyboard(project_tags: List[str], all_tags: List[str]) -> InlineKeyboardMarkup:
    """Клавиатура тегов проекта для удаления"""
    builder = InlineKeyboardBuilder()

    # Теги проекта для удаления
    for tag in project_tags:
        builder.add(
            InlineKeyboardButton(
                text=f"❌ #{tag}",
                callback_data=f"remove_tag_{tag}"
            )
        )

    if project_tags:
        builder.add(InlineKeyboardButton(text="─────────", callback_data="separator"))

    # Доступные теги для добавления
    available_tags = [tag for tag in all_tags if tag not in project_tags]
    for tag in available_tags[:10]:  # Показываем только первые 10
        builder.add(
            InlineKeyboardButton(
                text=f"➕ #{tag}",
                callback_data=f"add_tag_{tag}"
            )
        )

    builder.add(
        InlineKeyboardButton(text="✏️ Новый тег", callback_data="new_tag"),
        InlineKeyboardButton(text="✅ Готово", callback_data="tags_done"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    )

    builder.adjust(2)
    return builder.as_markup()


def confirm_delete_project_keyboard(project_id: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления проекта"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_project_{project_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="projects_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def project_details_keyboard(project_id: str) -> InlineKeyboardMarkup:
    """Клавиатура для детального просмотра проекта"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_project_{project_id}"),
        InlineKeyboardButton(text="🏷️ Управление тегами", callback_data=f"manage_project_tags_{project_id}"),
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_project_{project_id}"),
        InlineKeyboardButton(text="🔙 К списку", callback_data="projects_list")
    )
    builder.adjust(1, 1, 1, 1)
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


def back_to_projects_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к меню проектов"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 К проектам", callback_data="projects_menu"))
    return builder.as_markup()
