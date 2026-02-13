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
        genres: Optional[List[str]] = None
    ) -> VinylRecord:
        """Создать новую виниловую запись"""
        return await self.vinyl_repo.create(
            artist=artist,
            title=title,
            year=year,
            genres=genres or []
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
        genres: Optional[List[str]] = None
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

        if not update_data:
            return await self.get_vinyl_by_id(vinyl_id)

        return await self.vinyl_repo.update(vinyl_id, **update_data)

    async def delete_vinyl(self, vinyl_id: str) -> bool:
        """Удалить виниловую запись"""
        return await self.vinyl_repo.delete(vinyl_id)

    async def search_vinyl(self, query: str) -> List[VinylRecord]:
        """Поиск винила по исполнителю или названию"""
        all_vinyl = await self.get_all_vinyl()
        query_lower = query.lower()

        return [
            vinyl for vinyl in all_vinyl
            if query_lower in vinyl.artist.lower() or query_lower in vinyl.title.lower()
        ]

    # === HELPER METHODS ===

    async def format_vinyl_info(self, vinyl: VinylRecord) -> str:
        """Форматировать информацию о виниле для отображения"""
        info = f"🎵 *{vinyl.artist} - {vinyl.title}*\n"

        if vinyl.year:
            info += f"📅 Год: {vinyl.year}\n"

        if vinyl.genres:
            genres_str = ", ".join(vinyl.genres)
            info += f"🎭 Жанры: {genres_str}\n"

        return info

    async def get_all_genres(self) -> List[str]:
        """Получить все уникальные жанры"""
        all_vinyl = await self.get_all_vinyl()
        all_genres = set()

        for vinyl in all_vinyl:
            if vinyl.genres:
                all_genres.update(vinyl.genres)

        return sorted(list(all_genres))

    async def get_vinyl_by_genre(self, genre: str) -> List[VinylRecord]:
        """Получить винил по жанру"""
        all_vinyl = await self.get_all_vinyl()
        return [
            vinyl for vinyl in all_vinyl
            if vinyl.genres and genre in vinyl.genres
        ]

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
