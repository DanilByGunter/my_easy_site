from app.models.books import Book
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self, db):
        super().__init__(Book, db)
