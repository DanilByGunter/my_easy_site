from sqlalchemy import Column, String, JSON

from .common import Base, UUIDMixin


class Plant(Base, UUIDMixin):
    __tablename__ = "plants"

    family = Column(String, nullable=True)
    genus = Column(String, nullable=True)
    species = Column(String, nullable=True)
    common_name = Column(String, nullable=True)

    # Новое поле для галереи фотографий
    photos = Column(JSON, nullable=True)  # Массив объектов {url: str, date: str, notes?: str}
