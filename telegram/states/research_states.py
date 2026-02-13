"""
FSM состояния для управления исследованиями
"""
from aiogram.fsm.state import State, StatesGroup


class PublicationStates(StatesGroup):
    """Состояния для управления публикациями"""
    # Добавление публикации
    waiting_for_title = State()
    waiting_for_venue = State()
    waiting_for_year = State()
    waiting_for_url = State()

    # Редактирование публикации
    waiting_for_publication_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_title = State()
    waiting_for_edit_venue = State()
    waiting_for_edit_year = State()
    waiting_for_edit_url = State()

    # Удаление публикации
    waiting_for_delete_confirmation = State()

    # Поиск публикаций
    waiting_for_search_query = State()
    waiting_for_year_filter = State()
    waiting_for_venue_filter = State()


class InfographicStates(StatesGroup):
    """Состояния для управления инфографиками"""
    # Добавление инфографики
    waiting_for_title = State()
    waiting_for_topic = State()

    # Редактирование инфографики
    waiting_for_infographic_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_title = State()
    waiting_for_edit_topic = State()

    # Удаление инфографики
    waiting_for_delete_confirmation = State()

    # Поиск инфографик
    waiting_for_search_query = State()
    waiting_for_topic_filter = State()


class ResearchStates(StatesGroup):
    """Общие состояния для исследований"""
    # Выбор типа исследования
    waiting_for_research_type_selection = State()

    # Просмотр статистики
    viewing_statistics = State()
