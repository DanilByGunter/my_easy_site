"""
Сервис для работы с кофе в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.coffee import Coffee, CoffeeBrand, CoffeeReview  # noqa: E402
from app.repositories.coffee import (  # noqa: E402
    CoffeeRepository, CoffeeBrandRepository, CoffeeReviewRepository
)


class CoffeeService:
    """Сервис для управления кофе через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.coffee_repo = CoffeeRepository(db)
        self.brand_repo = CoffeeBrandRepository(db)
        self.review_repo = CoffeeReviewRepository(db)

    # === COFFEE BRANDS ===

    async def get_all_brands(self) -> List[CoffeeBrand]:
        """Получить все бренды кофе"""
        return await self.brand_repo.list()

    async def create_brand(self, name: str) -> CoffeeBrand:
        """Создать новый бренд кофе"""
        return await self.brand_repo.create(name=name)

    async def get_brand_by_id(self, brand_id: str) -> Optional[CoffeeBrand]:
        """Получить бренд по ID"""
        return await self.brand_repo.get_by_id(brand_id)

    async def update_brand(self, brand_id: str, name: str) -> Optional[CoffeeBrand]:
        """Обновить бренд"""
        return await self.brand_repo.update(brand_id, name=name)

    async def delete_brand(self, brand_id: str) -> bool:
        """Удалить бренд"""
        return await self.brand_repo.delete(brand_id)

    # === COFFEE ===

    async def get_all_coffees(self) -> List[Coffee]:
        """Получить все кофе с отзывами"""
        return await self.coffee_repo.list_with_reviews()

    async def get_coffees_by_brand(self, brand_id: str) -> List[Coffee]:
        """Получить кофе по бренду"""
        return await self.coffee_repo.list(brand_id=brand_id)

    async def create_coffee(
        self,
        brand_id: str,
        name: str,
        region: Optional[str] = None,
        processing: Optional[str] = None
    ) -> Coffee:
        """Создать новый кофе"""
        return await self.coffee_repo.create(
            brand_id=brand_id,
            name=name,
            region=region,
            processing=processing
        )

    async def get_coffee_by_id(self, coffee_id: str) -> Optional[Coffee]:
        """Получить кофе по ID"""
        return await self.coffee_repo.get_by_id(coffee_id)

    async def update_coffee(
        self,
        coffee_id: str,
        name: Optional[str] = None,
        region: Optional[str] = None,
        processing: Optional[str] = None
    ) -> Optional[Coffee]:
        """Обновить кофе"""
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if region is not None:
            update_data['region'] = region
        if processing is not None:
            update_data['processing'] = processing

        if not update_data:
            return await self.get_coffee_by_id(coffee_id)

        return await self.coffee_repo.update(coffee_id, **update_data)

    async def delete_coffee(self, coffee_id: str) -> bool:
        """Удалить кофе"""
        return await self.coffee_repo.delete(coffee_id)

    # === COFFEE REVIEWS ===

    async def create_review(
        self,
        coffee_id: str,
        method: str,
        rating: Optional[float] = None,
        notes: Optional[str] = None
    ) -> CoffeeReview:
        """Создать отзыв на кофе"""
        return await self.review_repo.create(
            coffee_id=coffee_id,
            method=method,
            rating=rating,
            notes=notes
        )

    async def get_reviews_by_coffee(self, coffee_id: str) -> List[CoffeeReview]:
        """Получить отзывы по кофе"""
        return await self.review_repo.list(coffee_id=coffee_id)

    async def update_review(
        self,
        review_id: str,
        method: Optional[str] = None,
        rating: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Optional[CoffeeReview]:
        """Обновить отзыв"""
        update_data = {}
        if method is not None:
            update_data['method'] = method
        if rating is not None:
            update_data['rating'] = rating
        if notes is not None:
            update_data['notes'] = notes

        if not update_data:
            return await self.review_repo.get_by_id(review_id)

        return await self.review_repo.update(review_id, **update_data)

    async def delete_review(self, review_id: str) -> bool:
        """Удалить отзыв"""
        return await self.review_repo.delete(review_id)

    # === HELPER METHODS ===

    async def format_coffee_info(self, coffee: Coffee) -> str:
        """Форматировать информацию о кофе для отображения"""
        info = f"☕ *{coffee.name}*\n"

        if coffee.brand:
            info += f"🏷️ Бренд: {coffee.brand.name}\n"

        if coffee.region:
            info += f"🌍 Регион: {coffee.region}\n"

        if coffee.processing:
            info += f"⚙️ Обработка: {coffee.processing}\n"

        if coffee.reviews:
            info += f"\n📝 *Отзывы ({len(coffee.reviews)}):*\n"
            for review in coffee.reviews:
                info += f"• {review.method}"
                if review.rating:
                    info += f" - {review.rating}/10"
                if review.notes:
                    info += f"\n  _{review.notes}_"
                info += "\n"

        return info

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
