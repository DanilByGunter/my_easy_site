"""
Сервис для работы с проектами в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.projects import Project  # noqa: E402
from app.repositories.projects import ProjectRepository  # noqa: E402


class ProjectsService:
    """Сервис для управления проектами через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repo = ProjectRepository(db)

    # === PROJECTS ===

    async def get_all_projects(self) -> List[Project]:
        """Получить все проекты"""
        return await self.project_repo.list()

    async def create_project(
        self,
        name: str,
        description: str,
        tags: Optional[List[str]] = None
    ) -> Project:
        """Создать новый проект"""
        return await self.project_repo.create(
            name=name,
            description=description,
            tags=tags or []
        )

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Получить проект по ID"""
        return await self.project_repo.get_by_id(project_id)

    async def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Project]:
        """Обновить проект"""
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description
        if tags is not None:
            update_data['tags'] = tags

        if not update_data:
            return await self.get_project_by_id(project_id)

        return await self.project_repo.update(project_id, **update_data)

    async def delete_project(self, project_id: str) -> bool:
        """Удалить проект"""
        return await self.project_repo.delete(project_id)

    async def search_projects(self, query: str) -> List[Project]:
        """Поиск проектов по названию или описанию"""
        all_projects = await self.get_all_projects()
        query_lower = query.lower()

        return [
            project for project in all_projects
            if (query_lower in project.name.lower()) or
            (query_lower in project.description.lower())
        ]

    async def get_projects_by_tag(self, tag: str) -> List[Project]:
        """Получить проекты по тегу"""
        all_projects = await self.get_all_projects()
        return [
            project for project in all_projects
            if project.tags and tag.lower() in [t.lower() for t in project.tags]
        ]

    # === HELPER METHODS ===

    async def format_project_info(self, project: Project) -> str:
        """Форматировать информацию о проекте для отображения"""
        info = f"🚀 *{project.name}*\n"
        info += f"📝 {project.description}\n"

        if project.tags:
            tags_str = ", ".join([f"#{tag}" for tag in project.tags])
            info += f"🏷️ Теги: {tags_str}\n"

        return info

    async def get_all_tags(self) -> List[str]:
        """Получить все уникальные теги"""
        all_projects = await self.get_all_projects()
        all_tags = set()

        for project in all_projects:
            if project.tags:
                all_tags.update(project.tags)

        return sorted(list(all_tags))

    async def get_projects_count_by_tag(self) -> dict:
        """Получить количество проектов по тегам"""
        all_projects = await self.get_all_projects()
        tag_counts = {}

        for project in all_projects:
            if project.tags:
                for tag in project.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return tag_counts

    async def add_tag_to_project(self, project_id: str, tag: str) -> Optional[Project]:
        """Добавить тег к проекту"""
        project = await self.get_project_by_id(project_id)
        if not project:
            return None

        tags = project.tags or []
        if tag not in tags:
            tags.append(tag)
            return await self.update_project(project_id, tags=tags)

        return project

    async def remove_tag_from_project(self, project_id: str, tag: str) -> Optional[Project]:
        """Удалить тег из проекта"""
        project = await self.get_project_by_id(project_id)
        if not project:
            return None

        tags = project.tags or []
        if tag in tags:
            tags.remove(tag)
            return await self.update_project(project_id, tags=tags)

        return project

    async def get_projects_without_tags(self) -> List[Project]:
        """Получить проекты без тегов"""
        all_projects = await self.get_all_projects()
        return [
            project for project in all_projects
            if not project.tags or len(project.tags) == 0
        ]

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
