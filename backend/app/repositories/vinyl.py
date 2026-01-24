from app.models.vinyl import VinylRecord
from app.repositories.base import BaseRepository


class VinylRepository(BaseRepository[VinylRecord]):
    def __init__(self, db):
        super().__init__(VinylRecord, db)
