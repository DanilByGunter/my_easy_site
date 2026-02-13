"""
Сервис для работы с растениями в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.plants import Plant  # noqa: E402
from app.repositories.plants import PlantRepository  # noqa: E402


class PlantsService:
    """Сервис для управления растениями через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.plant_repo = PlantRepository(db)

    # === PLANTS ===

    async def get_all_plants(self) -> List[Plant]:
        """Получить все растения"""
        return await self.plant_repo.list()

    async def create_plant(
        self,
        family: Optional[str] = None,
        genus: Optional[str] = None,
        species: Optional[str] = None,
        common_name: Optional[str] = None,
        photos: Optional[List[Dict[str, Any]]] = None
    ) -> Plant:
        """Создать новое растение"""
        return await self.plant_repo.create(
            family=family,
            genus=genus,
            species=species,
            common_name=common_name,
            photos=photos
        )

    async def get_plant_by_id(self, plant_id: str) -> Optional[Plant]:
        """Получить растение по ID"""
        return await self.plant_repo.get_by_id(plant_id)

    async def update_plant(
        self,
        plant_id: str,
        family: Optional[str] = None,
        genus: Optional[str] = None,
        species: Optional[str] = None,
        common_name: Optional[str] = None,
        photos: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Plant]:
        """Обновить растение"""
        update_data = {}
        if family is not None:
            update_data['family'] = family
        if genus is not None:
            update_data['genus'] = genus
        if species is not None:
            update_data['species'] = species
        if common_name is not None:
            update_data['common_name'] = common_name
        if photos is not None:
            update_data['photos'] = photos

        if not update_data:
            return await self.get_plant_by_id(plant_id)

        return await self.plant_repo.update(plant_id, **update_data)

    async def delete_plant(self, plant_id: str) -> bool:
        """Удалить растение"""
        return await self.plant_repo.delete(plant_id)

    async def search_plants(self, query: str) -> List[Plant]:
        """Поиск растений по любому полю"""
        all_plants = await self.get_all_plants()
        query_lower = query.lower()

        return [
            plant for plant in all_plants
            if (plant.family and query_lower in plant.family.lower()) or
            (plant.genus and query_lower in plant.genus.lower()) or
            (plant.species and query_lower in plant.species.lower()) or
            (plant.common_name and query_lower in plant.common_name.lower())
        ]

    async def get_plants_by_family(self, family: str) -> List[Plant]:
        """Получить растения по семейству"""
        all_plants = await self.get_all_plants()
        return [
            plant for plant in all_plants
            if plant.family and family.lower() in plant.family.lower()
        ]

    async def get_plants_by_genus(self, genus: str) -> List[Plant]:
        """Получить растения по роду"""
        all_plants = await self.get_all_plants()
        return [
            plant for plant in all_plants
            if plant.genus and genus.lower() in plant.genus.lower()
        ]

    # === HELPER METHODS ===

    async def format_plant_info(self, plant: Plant) -> str:
        """Форматировать информацию о растении для отображения"""
        info = "🌱 *Растение*\n"

        if plant.common_name:
            info += f"🏷️ Название: {plant.common_name}\n"

        if plant.family:
            info += f"👨‍👩‍👧‍👦 Семейство: {plant.family}\n"

        if plant.genus:
            info += f"🧬 Род: {plant.genus}\n"

        if plant.species:
            info += f"🔬 Вид: {plant.species}\n"

        if plant.photos:
            info += f"\n📸 *Фотографий: {len(plant.photos)}*\n"
            for i, photo in enumerate(plant.photos[:3], 1):  # Показываем только первые 3
                date = photo.get('date', 'Неизвестно')
                notes = photo.get('notes', '')
                info += f"{i}. {date}"
                if notes:
                    info += f" - _{notes}_"
                info += "\n"

            if len(plant.photos) > 3:
                info += f"... и еще {len(plant.photos) - 3} фото\n"

        return info

    async def get_scientific_name(self, plant: Plant) -> str:
        """Получить научное название растения"""
        parts = []
        if plant.genus:
            parts.append(plant.genus)
        if plant.species:
            parts.append(plant.species)

        if parts:
            return " ".join(parts)
        return "Неизвестно"

    async def get_all_families(self) -> List[str]:
        """Получить все уникальные семейства"""
        all_plants = await self.get_all_plants()
        families = set()

        for plant in all_plants:
            if plant.family:
                families.add(plant.family)

        return sorted(list(families))

    async def get_all_genera(self) -> List[str]:
        """Получить все уникальные роды"""
        all_plants = await self.get_all_plants()
        genera = set()

        for plant in all_plants:
            if plant.genus:
                genera.add(plant.genus)

        return sorted(list(genera))

    async def add_photo_to_plant(
        self,
        plant_id: str,
        url: str,
        date: str,
        notes: Optional[str] = None
    ) -> Optional[Plant]:
        """Добавить фотографию к растению"""
        plant = await self.get_plant_by_id(plant_id)
        if not plant:
            return None

        photos = plant.photos or []
        new_photo = {"url": url, "date": date}
        if notes:
            new_photo["notes"] = notes

        photos.append(new_photo)
        return await self.update_plant(plant_id, photos=photos)

    async def get_plants_with_photos(self) -> List[Plant]:
        """Получить растения с фотографиями"""
        all_plants = await self.get_all_plants()
        return [
            plant for plant in all_plants
            if plant.photos and len(plant.photos) > 0
        ]

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
