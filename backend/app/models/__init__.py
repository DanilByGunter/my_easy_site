# Import all models to ensure they are registered with SQLAlchemy
from .books import Book
from .coffee import Coffee, CoffeeBrand, CoffeeReview
from .common import Base
from .figures import Figure
from .media import MediaLink, SiteConfig
from .plants import Plant
from .projects import Project
from .research import Infographic, Publication
from .vinyl import VinylRecord

__all__ = [
    "Base",
    "Book",
    "Coffee",
    "CoffeeBrand",
    "CoffeeReview",
    "Figure",
    "MediaLink",
    "SiteConfig",
    "Plant",
    "Project",
    "Infographic",
    "Publication",
    "VinylRecord",
]
