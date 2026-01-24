from app.models.research import Infographic, Publication
from app.repositories.base import BaseRepository


class PublicationRepository(BaseRepository[Publication]):
    def __init__(self, db):
        super().__init__(Publication, db)


class InfographicRepository(BaseRepository[Infographic]):
    def __init__(self, db):
        super().__init__(Infographic, db)
