"""
Сервис для работы с фигурками в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.figures import Figure  # noqa: E402
from app.repositories.figures import FigureRepository  # noqa: E402


class FiguresService:
    """Сервис для управления фигурками через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.figure_repo = FigureRepository(db)

    # === FIGURES ===

    async def get_all_figures(self) -> List[Figure]:
        """Получить все фигурки"""
        return await self.figure_repo.list()

    async def create_figure(
        self,
        name: str,
        brand: str
    ) -> Figure:
        """Создать новую фигурку"""
        return await self.figure_repo.create(
            name=name,
            brand=brand
        )

    async def get_figure_by_id(self, figure_id: str) -> Optional[Figure]:
        """Получить фигурку по ID"""
        return await self.figure_repo.get_by_id(figure_id)

    async def update_figure(
        self,
        figure_id: str,
        name: Optional[str] = None,
        brand: Optional[str] = None
    ) -> Optional[Figure]:
        """Обновить фигурку"""
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if brand is not None:
            update_data['brand'] = brand

        if not update_data:
            return await self.get_figure_by_id(figure_id)

        return await self.figure_repo.update(figure_id, **update_data)

    async def delete_figure(self, figure_id: str) -> bool:
        """Удалить фигурку"""
        return await self.figure_repo.delete(figure_id)

    async def search_figures(self, query: str) -> List[Figure]:
        """Поиск фигурок по названию или бренду"""
        all_figures = await self.get_all_figures()
        query_lower = query.lower()

        return [
            figure for figure in all_figures
            if (query_lower in figure.name.lower()) or
            (query_lower in figure.brand.lower())
        ]

    async def get_figures_by_brand(self, brand: str) -> List[Figure]:
        """Получить фигурки по бренду"""
        all_figures = await self.get_all_figures()
        return [
            figure for figure in all_figures
            if brand.lower() in figure.brand.lower()
        ]

    # === HELPER METHODS ===

    async def format_figure_info(self, figure: Figure) -> str:
        """Форматировать информацию о фигурке для отображения"""
        info = f"🎭 *{figure.name}*\n"
        info += f"🏷️ Бренд: {figure.brand}\n"

        return info

    async def get_all_brands(self) -> List[str]:
        """Получить все уникальные бренды"""
        all_figures = await self.get_all_figures()
        brands = set()

        for figure in all_figures:
            brands.add(figure.brand)

        return sorted(list(brands))

    async def get_figures_count_by_brand(self) -> dict:
        """Получить количество фигурок по брендам"""
        all_figures = await self.get_all_figures()
        brand_counts = {}

        for figure in all_figures:
            brand_counts[figure.brand] = brand_counts.get(figure.brand, 0) + 1

        return brand_counts

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
