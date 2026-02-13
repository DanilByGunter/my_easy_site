"""
FSM состояния для управления проектами
"""
from aiogram.fsm.state import State, StatesGroup


class ProjectsStates(StatesGroup):
    """Состояния для управления проектами"""
    # Добавление проекта
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_tags = State()

    # Редактирование проекта
    waiting_for_project_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_name = State()
    waiting_for_edit_description = State()
    waiting_for_edit_tags = State()

    # Удаление проекта
    waiting_for_delete_confirmation = State()

    # Поиск проектов
    waiting_for_search_query = State()
    waiting_for_tag_filter = State()

    # Управление тегами
    waiting_for_tag_project_selection = State()
    waiting_for_new_tag = State()
    waiting_for_tag_to_remove = State()
