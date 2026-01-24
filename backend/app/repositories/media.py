from app.models.media import MediaLink, SiteConfig
from app.repositories.base import BaseRepository


class MediaLinkRepository(BaseRepository[MediaLink]):
    def __init__(self, db):
        super().__init__(MediaLink, db)


class SiteConfigRepository(BaseRepository[SiteConfig]):
    def __init__(self, db):
        super().__init__(SiteConfig, db)
