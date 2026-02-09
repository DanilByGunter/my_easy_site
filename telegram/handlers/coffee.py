"""
Обработчики для управления кофе
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import get_db_session
from services.coffee_service import CoffeeService
from states.coffee_states import CoffeeBrandStates, CoffeeStates
from keyboards.coffee_keyboards import (
    coffee_brands_keyboard, coffee_list_keyboard,
    brands_selection_keyboard, cancel_keyboard, skip_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


# === БРЕНДЫ КОФЕ ===

@router.callback_query(F.data == "coffee_brands")
async def show_brands_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления брендами"""
    await state.clear()

    await callback.message.edit_text(
        "🏷️ *Управление брендами кофе*\n\n"
        "Выберите действие:",
        reply_markup=coffee_brands_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "brands_list")
async def show_brands_list(callback: CallbackQuery):
    """Показать список всех брендов"""
    async with get_db_session() as db:
        service = CoffeeService(db)
        brands = await service.get_all_brands()

    if not brands:
        text = "📋 *Список брендов*\n\n❌ Бренды не найдены"
    else:
        text = "📋 *Список брендов:*\n\n"
        for i, brand in enumerate(brands, 1):
            text += f"{i}. {brand.name}\n"

    await callback.message.edit_text(
        text,
        reply_markup=coffee_brands_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "brand_add")
async def start_add_brand(callback: CallbackQuery, state: FSMContext):
    """Начать добавление нового бренда"""
    await state.set_state(CoffeeBrandStates.waiting_for_brand_name)

    await callback.message.edit_text(
        "➕ *Добавление нового бренда*\n\n"
        "Введите название бренда:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(CoffeeBrandStates.waiting_for_brand_name)
async def process_brand_name(message: Message, state: FSMContext):
    """Обработать название бренда"""
    brand_name = message.text.strip()

    if not brand_name:
        await message.answer(
            "❌ Название бренда не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    try:
        async with get_db_session() as db:
            service = CoffeeService(db)
            brand = await service.create_brand(brand_name)
            await service.commit()

        await state.clear()
        await message.answer(
            f"✅ *Бренд добавлен!*\n\n"
            f"🏷️ Название: {brand.name}",
            reply_markup=coffee_brands_keyboard(),
            parse_mode="Markdown"
        )

        logger.info(f"Добавлен новый бренд: {brand.name}")

    except Exception as e:
        logger.error(f"Ошибка при добавлении бренда: {e}")
        await message.answer(
            "❌ Произошла ошибка при добавлении бренда. "
            "Возможно, бренд с таким названием уже существует.",
            reply_markup=coffee_brands_keyboard()
        )
        await state.clear()


# === КОФЕ ===

@router.callback_query(F.data == "coffee_list")
async def show_coffee_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню управления кофе"""
    await state.clear()

    await callback.message.edit_text(
        "☕ *Управление кофе*\n\n"
        "Выберите действие:",
        reply_markup=coffee_list_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "coffee_show_list")
async def show_coffee_list(callback: CallbackQuery):
    """Показать список всего кофе"""
    async with get_db_session() as db:
        service = CoffeeService(db)
        coffees = await service.get_all_coffees()

    if not coffees:
        text = "📋 *Список кофе*\n\n❌ Кофе не найден"
    else:
        text = "📋 *Список кофе:*\n\n"
        for i, coffee in enumerate(coffees, 1):
            brand_name = coffee.brand.name if coffee.brand else "Неизвестный бренд"
            text += f"{i}. *{coffee.name}* ({brand_name})\n"
            if coffee.region:
                text += f"   🌍 {coffee.region}\n"
            if coffee.reviews:
                text += f"   📝 Отзывов: {len(coffee.reviews)}\n"
            text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=coffee_list_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "coffee_add")
async def start_add_coffee(callback: CallbackQuery, state: FSMContext):
    """Начать добавление нового кофе"""
    # Получаем список брендов
    async with get_db_session() as db:
        service = CoffeeService(db)
        brands = await service.get_all_brands()

    if not brands:
        await callback.message.edit_text(
            "❌ *Нет доступных брендов*\n\n"
            "Сначала добавьте хотя бы один бренд кофе.",
            reply_markup=coffee_brands_keyboard(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Сохраняем бренды в состояние
    brands_data = [{"id": str(brand.id), "name": brand.name} for brand in brands]
    await state.update_data(brands=brands_data)
    await state.set_state(CoffeeStates.waiting_for_brand_selection)

    await callback.message.edit_text(
        "➕ *Добавление нового кофе*\n\n"
        "Выберите бренд:",
        reply_markup=brands_selection_keyboard(brands_data),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_brand_"))
async def process_brand_selection(callback: CallbackQuery, state: FSMContext):
    """Обработать выбор бренда"""
    brand_id = callback.data.split("_")[-1]

    # Сохраняем выбранный бренд
    await state.update_data(selected_brand_id=brand_id)
    await state.set_state(CoffeeStates.waiting_for_coffee_name)

    await callback.message.edit_text(
        "☕ *Добавление нового кофе*\n\n"
        "Введите название кофе:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(CoffeeStates.waiting_for_coffee_name)
async def process_coffee_name(message: Message, state: FSMContext):
    """Обработать название кофе"""
    coffee_name = message.text.strip()

    if not coffee_name:
        await message.answer(
            "❌ Название кофе не может быть пустым. Попробуйте еще раз:",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(coffee_name=coffee_name)
    await state.set_state(CoffeeStates.waiting_for_coffee_region)

    await message.answer(
        "🌍 *Регион происхождения*\n\n"
        "Введите регион происхождения кофе (например: Эфиопия, Колумбия):",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )


@router.message(CoffeeStates.waiting_for_coffee_region)
async def process_coffee_region(message: Message, state: FSMContext):
    """Обработать регион кофе"""
    region = message.text.strip() if message.text.strip() else None

    await state.update_data(coffee_region=region)
    await state.set_state(CoffeeStates.waiting_for_coffee_processing)

    await message.answer(
        "⚙️ *Способ обработки*\n\n"
        "Введите способ обработки (например: мытая, натуральная, хани):",
        reply_markup=skip_keyboard(),
        parse_mode="Markdown"
    )


@router.message(CoffeeStates.waiting_for_coffee_processing)
async def process_coffee_processing(message: Message, state: FSMContext):
    """Обработать способ обработки и создать кофе"""
    processing = message.text.strip() if message.text.strip() else None

    # Получаем все данные из состояния
    data = await state.get_data()

    try:
        async with get_db_session() as db:
            service = CoffeeService(db)
            coffee = await service.create_coffee(
                brand_id=data['selected_brand_id'],
                name=data['coffee_name'],
                region=data.get('coffee_region'),
                processing=processing
            )
            await service.commit()

        await state.clear()

        # Форматируем информацию о созданном кофе
        info = "✅ *Кофе добавлен!*\n\n"
        info += f"☕ *{coffee.name}*\n"
        if coffee.region:
            info += f"🌍 Регион: {coffee.region}\n"
        if processing:
            info += f"⚙️ Обработка: {processing}\n"

        await message.answer(
            info,
            reply_markup=coffee_list_keyboard(),
            parse_mode="Markdown"
        )

        logger.info(f"Добавлен новый кофе: {coffee.name}")

    except Exception as e:
        logger.error(f"Ошибка при добавлении кофе: {e}")
        await message.answer(
            "❌ Произошла ошибка при добавлении кофе.",
            reply_markup=coffee_list_keyboard()
        )
        await state.clear()


@router.callback_query(F.data == "skip_field")
async def skip_field(callback: CallbackQuery, state: FSMContext):
    """Пропустить поле"""
    current_state = await state.get_state()

    if current_state == CoffeeStates.waiting_for_coffee_region.state:
        await state.update_data(coffee_region=None)
        await state.set_state(CoffeeStates.waiting_for_coffee_processing)

        await callback.message.edit_text(
            "⚙️ *Способ обработки*\n\n"
            "Введите способ обработки (например: мытая, натуральная, хани):",
            reply_markup=skip_keyboard(),
            parse_mode="Markdown"
        )

    elif current_state == CoffeeStates.waiting_for_coffee_processing.state:
        # Создаем кофе без обработки
        data = await state.get_data()

        try:
            async with get_db_session() as db:
                service = CoffeeService(db)
                coffee = await service.create_coffee(
                    brand_id=data['selected_brand_id'],
                    name=data['coffee_name'],
                    region=data.get('coffee_region'),
                    processing=None
                )
                await service.commit()

            await state.clear()

            info = "✅ *Кофе добавлен!*\n\n"
            info += f"☕ *{coffee.name}*\n"
            if coffee.region:
                info += f"🌍 Регион: {coffee.region}\n"

            await callback.message.edit_text(
                info,
                reply_markup=coffee_list_keyboard(),
                parse_mode="Markdown"
            )

            logger.info(f"Добавлен новый кофе: {coffee.name}")

        except Exception as e:
            logger.error(f"Ошибка при добавлении кофе: {e}")
            await callback.message.edit_text(
                "❌ Произошла ошибка при добавлении кофе.",
                reply_markup=coffee_list_keyboard()
            )
            await state.clear()

    await callback.answer("Поле пропущено")
