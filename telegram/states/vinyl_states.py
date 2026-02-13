"""
FSM состояния для управления винилом
"""
from aiogram.fsm.state import State, StatesGroup


class VinylStates(StatesGroup):
    """Состояния для управления винилом"""
    # Добавление винила
    waiting_for_artist = State()
    waiting_for_title = State()
    waiting_for_year = State()
    waiting_for_genres = State()

    # Редактирование винила
    waiting_for_vinyl_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_artist = State()
    waiting_for_edit_title = State()
    waiting_for_edit_year = State()
    waiting_for_edit_genres = State()

    # Удаление винила
    waiting_for_delete_confirmation = State()

    # Поиск винила
    waiting_for_search_query = State()
    waiting_for_genre_selection = State()
