from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.books import BookRepository
from app.repositories.coffee import CoffeeBrandRepository, CoffeeRepository
from app.repositories.figures import FigureRepository
from app.repositories.media import MediaLinkRepository, SiteConfigRepository
from app.repositories.plants import PlantRepository
from app.repositories.projects import ProjectRepository
from app.repositories.research import InfographicRepository, PublicationRepository
from app.repositories.vinyl import VinylRepository


class AllDataService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vinyl_repo = VinylRepository(db)
        self.book_repo = BookRepository(db)
        self.coffee_repo = CoffeeRepository(db)
        self.coffee_brand_repo = CoffeeBrandRepository(db)
        self.figure_repo = FigureRepository(db)
        self.project_repo = ProjectRepository(db)
        self.publication_repo = PublicationRepository(db)
        self.infographic_repo = InfographicRepository(db)
        self.plant_repo = PlantRepository(db)
        self.media_link_repo = MediaLinkRepository(db)
        self.site_config_repo = SiteConfigRepository(db)

    async def get_all_data(self) -> dict:
        """Aggregate all data and return as dict matching frontend contract"""

        try:
            # Fetch all data in parallel
            vinyl_records = await self.vinyl_repo.list() or []
            books = await self.book_repo.list() or []
            coffees = await self.coffee_repo.list_with_reviews() or []
            coffee_brands = await self.coffee_brand_repo.list() or []
            figures = await self.figure_repo.list() or []
            projects = await self.project_repo.list() or []
            publications = await self.publication_repo.list() or []
            infographics = await self.infographic_repo.list() or []
            plants = await self.plant_repo.list() or []
            media_links = await self.media_link_repo.list() or []
            site_config = await self.site_config_repo.list() or []

            site_config = site_config[0] if site_config else None
        except Exception as e:
            # Log the error and return empty data structure
            print(f"Error fetching data: {e}")
            # Return empty data structure that matches frontend expectations
            return {
                "about": {"bio": ""},
                "vinylGenres": [],
                "vinyl": [],
                "books": [],
                "coffeeBrands": [],
                "coffee": [],
                "figures": [],
                "projects": [],
                "publications": [],
                "infographics": [],
                "plants": [],
                "media": {
                    "externalWishUrl": "",
                    "links": [],
                },
            }

        # Build response structure
        result = {
            "about": {"bio": site_config.about_bio if site_config else ""},
            "vinylGenres": self._extract_vinyl_genres(vinyl_records),
            "vinyl": [self._map_vinyl(record) for record in vinyl_records],
            "books": [self._map_book(book) for book in books],
            "coffeeBrands": [self._map_coffee_brand(brand) for brand in coffee_brands],
            "coffee": [self._map_coffee(coffee) for coffee in coffees],
            "figures": [self._map_figure(figure) for figure in figures],
            "projects": [self._map_project(project) for project in projects],
            "publications": [self._map_publication(pub) for pub in publications],
            "infographics": [self._map_infographic(info) for info in infographics],
            "plants": [self._map_plant(plant) for plant in plants],
            "media": {
                "externalWishUrl": site_config.external_wish_url if site_config else "",
                "links": [self._map_media_link(link) for link in media_links],
            },
        }

        return result

    def _extract_vinyl_genres(self, vinyl_records) -> list[str]:
        """Extract unique genres from all vinyl records"""
        all_genres = set()
        for record in vinyl_records:
            all_genres.update(record.genres or [])
        return sorted(list(all_genres))

    def _map_vinyl(self, record) -> dict:
        """Map vinyl record to frontend format"""
        return {
            "id": str(record.id),
            "artist": record.artist,
            "title": record.title,
            "year": record.year,
            "genres": record.genres or [],
            "photo_url": record.photo_url,
        }

    def _map_book(self, book) -> dict:
        """Map book to frontend format"""
        return {
            "id": str(book.id),
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "language": book.language,
            "format": book.format,
            "review": book.review,
        }

    def _map_coffee_brand(self, brand) -> dict:
        """Map coffee brand to frontend format"""
        return {"id": str(brand.id), "name": brand.name}

    def _map_coffee(self, coffee) -> dict:
        """Map coffee to frontend format"""
        return {
            "id": str(coffee.id),
            "brandId": str(coffee.brand_id),
            "name": coffee.name,
            "region": coffee.region,
            "processing": coffee.processing,
            "reviews": [self._map_coffee_review(review) for review in coffee.reviews],
        }

    def _map_coffee_review(self, review) -> dict:
        """Map coffee review to frontend format"""
        return {"method": review.method, "rating": review.rating, "notes": review.notes}

    def _map_figure(self, figure) -> dict:
        """Map figure to frontend format"""
        return {"id": str(figure.id), "name": figure.name, "brand": figure.brand}

    def _map_project(self, project) -> dict:
        """Map project to frontend format"""
        return {
            "id": str(project.id),
            "name": project.name,
            "desc": project.description,
            "tags": project.tags or [],
        }

    def _map_publication(self, publication) -> dict:
        """Map publication to frontend format"""
        return {
            "id": str(publication.id),
            "title": publication.title,
            "venue": publication.venue,
            "year": publication.year,
            "url": publication.url,
        }

    def _map_infographic(self, infographic) -> dict:
        """Map infographic to frontend format"""
        return {
            "id": str(infographic.id),
            "topic": infographic.topic,
            "title": infographic.title,
        }

    def _map_plant(self, plant) -> dict:
        """Map plant to frontend format"""
        return {
            "id": str(plant.id),
            "family": plant.family,
            "genus": plant.genus,
            "species": plant.species,
            "commonName": plant.common_name,
        }

    def _map_media_link(self, link) -> dict:
        """Map media link to frontend format"""
        return {"type": link.type, "label": link.label, "value": link.value}
