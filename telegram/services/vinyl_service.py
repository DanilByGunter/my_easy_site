"""
Сервис для работы с винилом в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.vinyl import VinylRecord  # noqa: E402
from app.repositories.vinyl import VinylRepository  # noqa: E402


class VinylService:
    """Сервис для управления винилом через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.vinyl_repo = VinylRepository(db)

    # === VINYL RECORDS ===

    async def get_all_vinyl(self) -> List[VinylRecord]:
        """Получить все виниловые записи"""
        return await self.vinyl_repo.list()

    async def create_vinyl(
        self,
        artist: str,
        title: str,
        year: Optional[int] = None,
        genres: Optional[List[str]] = None,
        photo_url: Optional[str] = None
    ) -> VinylRecord:
        """Создать новую виниловую запись"""
        return await self.vinyl_repo.create(
            artist=artist,
            title=title,
            year=year,
            genres=genres or [],
            photo_url=photo_url
        )

    async def get_vinyl_by_id(self, vinyl_id: str) -> Optional[VinylRecord]:
        """Получить винил по ID"""
        return await self.vinyl_repo.get_by_id(vinyl_id)

    async def update_vinyl(
        self,
        vinyl_id: str,
        artist: Optional[str] = None,
        title: Optional[str] = None,
        year: Optional[int] = None,
        genres: Optional[List[str]] = None,
        photo_url: Optional[str] = None
    ) -> Optional[VinylRecord]:
        """Обновить виниловую запись"""
        update_data = {}
        if artist is not None:
            update_data['artist'] = artist
        if title is not None:
            update_data['title'] = title
        if year is not None:
            update_data['year'] = year
        if genres is not None:
            update_data['genres'] = genres
        if photo_url is not None:
            update_data['photo_url'] = photo_url

        if not update_data:
            return await self.get_vinyl_by_id(vinyl_id)

        return await self.vinyl_repo.update(vinyl_id, **update_data)

    async def delete_vinyl(self, vinyl_id: str) -> bool:
        """Удалить виниловую запись"""
        return await self.vinyl_repo.delete(vinyl_id)

    # === HELPER METHODS ===

    async def format_vinyl_info(self, vinyl: VinylRecord) -> str:
        """Форматировать информацию о виниле для отображения"""
        info = f"🎵 *{vinyl.artist} - {vinyl.title}*\n"

        if vinyl.year:
            info += f"📅 Год: {vinyl.year}\n"

        if vinyl.genres:
            genres_str = ", ".join(vinyl.genres)
            info += f"🎭 Жанры: {genres_str}\n"

        if hasattr(vinyl, 'photo_url') and vinyl.photo_url:
            info += "📸 Фото: есть\n"

        return info

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
