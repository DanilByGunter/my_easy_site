from app.models.projects import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db):
        super().__init__(Project, db)
