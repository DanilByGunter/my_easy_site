from app.models.figures import Figure
from app.repositories.base import BaseRepository


class FigureRepository(BaseRepository[Figure]):
    def __init__(self, db):
        super().__init__(Figure, db)
