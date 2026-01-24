from sqlalchemy import ARRAY, Column, String

from .common import Base, UUIDMixin


class Project(Base, UUIDMixin):
    __tablename__ = "projects"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False, default=list)
