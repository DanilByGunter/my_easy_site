from sqlalchemy import Column, String

from .common import Base, UUIDMixin


class Book(Base, UUIDMixin):
    __tablename__ = "books"

    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    language = Column(String, nullable=True)
    format = Column(String, nullable=True)
    review = Column(String, nullable=True)
