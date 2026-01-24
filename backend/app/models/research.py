from sqlalchemy import Column, Integer, String

from .common import Base, UUIDMixin


class Publication(Base, UUIDMixin):
    __tablename__ = "publications"

    title = Column(String, nullable=False)
    venue = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    url = Column(String, nullable=True)


class Infographic(Base, UUIDMixin):
    __tablename__ = "infographics"

    topic = Column(String, nullable=True)
    title = Column(String, nullable=False)
