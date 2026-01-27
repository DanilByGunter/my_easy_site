from sqlalchemy import Column, String, Text, JSON

from .common import Base, UUIDMixin


class Book(Base, UUIDMixin):
    __tablename__ = "books"

    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    language = Column(String, nullable=True)
    format = Column(String, nullable=True)
    review = Column(String, nullable=True)

    # Новые поля для цитат и авторского мнения
    quotes = Column(JSON, nullable=True)  # Массив объектов {text: str, page?: int}
    opinion = Column(Text, nullable=True)  # Авторское мнение о книге
