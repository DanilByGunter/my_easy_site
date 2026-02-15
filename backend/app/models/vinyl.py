from sqlalchemy import ARRAY, Column, Integer, String

from .common import Base, UUIDMixin


class VinylRecord(Base, UUIDMixin):
    __tablename__ = "vinyl_records"

    artist = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    genres = Column(ARRAY(String), nullable=False, default=list)
    photo_url = Column(String, nullable=True)  # URL фото в S3
