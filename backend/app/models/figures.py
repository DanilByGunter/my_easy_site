from sqlalchemy import Column, String

from .common import Base, UUIDMixin


class Figure(Base, UUIDMixin):
    __tablename__ = "figures"

    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
