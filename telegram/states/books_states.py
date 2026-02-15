"""
FSM состояния для управления книгами
"""
from aiogram.fsm.state import State, StatesGroup


class BooksStates(StatesGroup):
    """Состояния для управления книгами"""
    # Добавление книги
    waiting_for_title = State()
    waiting_for_author = State()
    waiting_for_genre = State()
    waiting_for_language = State()
    waiting_for_format = State()
    waiting_for_review = State()
    waiting_for_opinion = State()

    # Редактирование книги
    waiting_for_book_selection = State()
    waiting_for_edit_field_selection = State()
    waiting_for_edit_title = State()
    waiting_for_edit_author = State()
    waiting_for_edit_genre = State()
    waiting_for_edit_language = State()
    waiting_for_edit_format = State()
    waiting_for_edit_review = State()
    waiting_for_edit_opinion = State()

    # Удаление книги
    waiting_for_delete_selection = State()
    waiting_for_delete_confirmation = State()

    # Управление цитатами
    waiting_for_quote_book_selection = State()
    waiting_for_quote_text = State()
    waiting_for_quote_page = State()
