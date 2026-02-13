"""
Сервис для работы с исследованиями в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.research import Publication, Infographic  # noqa: E402
from app.repositories.research import PublicationRepository, InfographicRepository  # noqa: E402


class ResearchService:
    """Сервис для управления исследованиями через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.publication_repo = PublicationRepository(db)
        self.infographic_repo = InfographicRepository(db)

    # === PUBLICATIONS ===

    async def get_all_publications(self) -> List[Publication]:
        """Получить все публикации"""
        return await self.publication_repo.list()

    async def create_publication(
        self,
        title: str,
        venue: Optional[str] = None,
        year: Optional[int] = None,
        url: Optional[str] = None
    ) -> Publication:
        """Создать новую публикацию"""
        return await self.publication_repo.create(
            title=title,
            venue=venue,
            year=year,
            url=url
        )

    async def get_publication_by_id(self, publication_id: str) -> Optional[Publication]:
        """Получить публикацию по ID"""
        return await self.publication_repo.get_by_id(publication_id)

    async def update_publication(
        self,
        publication_id: str,
        title: Optional[str] = None,
        venue: Optional[str] = None,
        year: Optional[int] = None,
        url: Optional[str] = None
    ) -> Optional[Publication]:
        """Обновить публикацию"""
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if venue is not None:
            update_data['venue'] = venue
        if year is not None:
            update_data['year'] = year
        if url is not None:
            update_data['url'] = url

        if not update_data:
            return await self.get_publication_by_id(publication_id)

        return await self.publication_repo.update(publication_id, **update_data)

    async def delete_publication(self, publication_id: str) -> bool:
        """Удалить публикацию"""
        return await self.publication_repo.delete(publication_id)

    async def search_publications(self, query: str) -> List[Publication]:
        """Поиск публикаций по названию или месту публикации"""
        all_publications = await self.get_all_publications()
        query_lower = query.lower()

        return [
            pub for pub in all_publications
            if (query_lower in pub.title.lower()) or
            (pub.venue and query_lower in pub.venue.lower())
        ]

    async def get_publications_by_year(self, year: int) -> List[Publication]:
        """Получить публикации по году"""
        all_publications = await self.get_all_publications()
        return [
            pub for pub in all_publications
            if pub.year == year
        ]

    async def get_publications_by_venue(self, venue: str) -> List[Publication]:
        """Получить публикации по месту публикации"""
        all_publications = await self.get_all_publications()
        return [
            pub for pub in all_publications
            if pub.venue and venue.lower() in pub.venue.lower()
        ]

    # === INFOGRAPHICS ===

    async def get_all_infographics(self) -> List[Infographic]:
        """Получить все инфографики"""
        return await self.infographic_repo.list()

    async def create_infographic(
        self,
        title: str,
        topic: Optional[str] = None
    ) -> Infographic:
        """Создать новую инфографику"""
        return await self.infographic_repo.create(
            title=title,
            topic=topic
        )

    async def get_infographic_by_id(self, infographic_id: str) -> Optional[Infographic]:
        """Получить инфографику по ID"""
        return await self.infographic_repo.get_by_id(infographic_id)

    async def update_infographic(
        self,
        infographic_id: str,
        title: Optional[str] = None,
        topic: Optional[str] = None
    ) -> Optional[Infographic]:
        """Обновить инфографику"""
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if topic is not None:
            update_data['topic'] = topic

        if not update_data:
            return await self.get_infographic_by_id(infographic_id)

        return await self.infographic_repo.update(infographic_id, **update_data)

    async def delete_infographic(self, infographic_id: str) -> bool:
        """Удалить инфографику"""
        return await self.infographic_repo.delete(infographic_id)

    async def search_infographics(self, query: str) -> List[Infographic]:
        """Поиск инфографик по названию или теме"""
        all_infographics = await self.get_all_infographics()
        query_lower = query.lower()

        return [
            info for info in all_infographics
            if (query_lower in info.title.lower()) or
            (info.topic and query_lower in info.topic.lower())
        ]

    async def get_infographics_by_topic(self, topic: str) -> List[Infographic]:
        """Получить инфографики по теме"""
        all_infographics = await self.get_all_infographics()
        return [
            info for info in all_infographics
            if info.topic and topic.lower() in info.topic.lower()
        ]

    # === HELPER METHODS ===

    async def format_publication_info(self, publication: Publication) -> str:
        """Форматировать информацию о публикации для отображения"""
        info = f"📄 *{publication.title}*\n"

        if publication.venue:
            info += f"🏛️ Место: {publication.venue}\n"

        if publication.year:
            info += f"📅 Год: {publication.year}\n"

        if publication.url:
            info += f"🔗 [Ссылка]({publication.url})\n"

        return info

    async def format_infographic_info(self, infographic: Infographic) -> str:
        """Форматировать информацию об инфографике для отображения"""
        info = f"📊 *{infographic.title}*\n"

        if infographic.topic:
            info += f"🏷️ Тема: {infographic.topic}\n"

        return info

    async def get_all_publication_years(self) -> List[int]:
        """Получить все уникальные годы публикаций"""
        all_publications = await self.get_all_publications()
        years = set()

        for pub in all_publications:
            if pub.year:
                years.add(pub.year)

        return sorted(list(years), reverse=True)

    async def get_all_venues(self) -> List[str]:
        """Получить все уникальные места публикаций"""
        all_publications = await self.get_all_publications()
        venues = set()

        for pub in all_publications:
            if pub.venue:
                venues.add(pub.venue)

        return sorted(list(venues))

    async def get_all_topics(self) -> List[str]:
        """Получить все уникальные темы инфографик"""
        all_infographics = await self.get_all_infographics()
        topics = set()

        for info in all_infographics:
            if info.topic:
                topics.add(info.topic)

        return sorted(list(topics))

    async def get_publications_count_by_year(self) -> dict:
        """Получить количество публикаций по годам"""
        all_publications = await self.get_all_publications()
        year_counts = {}

        for pub in all_publications:
            if pub.year:
                year_counts[pub.year] = year_counts.get(pub.year, 0) + 1

        return year_counts

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
