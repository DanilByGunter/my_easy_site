"""
FSM состояния для управления растениями
"""
from aiogram.fsm.state import State, StatesGroup


class PlantsStates(StatesGroup):
    """Состояния для управления растениями"""
    # Добавление растения
    waiting_for_common_name = State()
    waiting_for_family = State()
    waiting_for_genus = State()
    waiting_for_species = State()

    # Редактирование растения
    waiting_for_plant_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_common_name = State()
    waiting_for_edit_family = State()
    waiting_for_edit_genus = State()
    waiting_for_edit_species = State()

    # Удаление растения
    waiting_for_delete_confirmation = State()

    # Поиск растений
    waiting_for_search_query = State()
    waiting_for_family_filter = State()
    waiting_for_genus_filter = State()

    # Управление фотографиями
    waiting_for_photo_plant_selection = State()
    waiting_for_photo_url = State()
    waiting_for_photo_date = State()
    waiting_for_photo_notes = State()
