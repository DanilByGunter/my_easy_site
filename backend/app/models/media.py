from sqlalchemy import Column, String

from .common import Base, UUIDMixin


class MediaLink(Base, UUIDMixin):
    __tablename__ = "media_links"

    type = Column(String, nullable=False)  # Telegram, GitHub, Email, etc.
    label = Column(String, nullable=True)
    value = Column(String, nullable=False)


class SiteConfig(Base, UUIDMixin):
    __tablename__ = "site_config"

    external_wish_url = Column(String, nullable=False)
    about_bio = Column(String, nullable=False)
