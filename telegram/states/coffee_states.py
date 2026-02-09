"""
FSM состояния для управления кофе
"""
from aiogram.fsm.state import State, StatesGroup


class CoffeeBrandStates(StatesGroup):
    """Состояния для управления брендами кофе"""
    waiting_for_brand_name = State()
    waiting_for_brand_edit_name = State()
    waiting_for_brand_delete_confirm = State()


class CoffeeStates(StatesGroup):
    """Состояния для управления кофе"""
    waiting_for_brand_selection = State()
    waiting_for_coffee_name = State()
    waiting_for_coffee_region = State()
    waiting_for_coffee_processing = State()

    # Редактирование кофе
    waiting_for_coffee_edit_selection = State()
    waiting_for_coffee_edit_name = State()
    waiting_for_coffee_edit_region = State()
    waiting_for_coffee_edit_processing = State()

    # Удаление кофе
    waiting_for_coffee_delete_confirm = State()


class CoffeeReviewStates(StatesGroup):
    """Состояния для управления отзывов на кофе"""
    waiting_for_coffee_selection = State()
    waiting_for_review_method = State()
    waiting_for_review_rating = State()
    waiting_for_review_notes = State()

    # Редактирование отзыва
    waiting_for_review_edit_selection = State()
    waiting_for_review_edit_method = State()
    waiting_for_review_edit_rating = State()
    waiting_for_review_edit_notes = State()

    # Удаление отзыва
    waiting_for_review_delete_confirm = State()
