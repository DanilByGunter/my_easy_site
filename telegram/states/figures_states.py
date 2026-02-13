"""
FSM состояния для управления фигурками
"""
from aiogram.fsm.state import State, StatesGroup


class FiguresStates(StatesGroup):
    """Состояния для управления фигурками"""
    # Добавление фигурки
    waiting_for_name = State()
    waiting_for_brand = State()

    # Редактирование фигурки
    waiting_for_figure_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_name = State()
    waiting_for_edit_brand = State()

    # Удаление фигурки
    waiting_for_delete_confirmation = State()

    # Поиск фигурок
    waiting_for_search_query = State()
    waiting_for_brand_filter = State()
