from app.models.plants import Plant
from app.repositories.base import BaseRepository


class PlantRepository(BaseRepository[Plant]):
    def __init__(self, db):
        super().__init__(Plant, db)
