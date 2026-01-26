import asyncio
import os

from app.models.books import Book
from app.models.coffee import Coffee, CoffeeBrand, CoffeeReview
from app.models.common import Base
from app.models.figures import Figure
from app.models.media import MediaLink, SiteConfig
from app.models.plants import Plant
from app.models.projects import Project
from app.models.research import Infographic, Publication
from app.models.vinyl import VinylRecord
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Construct from individual environment variables
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")

    if not all([postgres_user, postgres_password, postgres_db]):
        raise ValueError("Database connection parameters not found in environment variables. "
                         "Please set POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB.")

    DATABASE_URL = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_data():
    async with AsyncSessionLocal() as session:
        # Site config
        site_config = SiteConfig(
            external_wish_url="https://example.com/my-wishlist",
            about_bio="Личный сайт с моими интересами: винил, книги, кофе, фигурки, проекты, исследования, растения и контакты. Всё, что здесь — уже есть у меня.",
        )
        session.add(site_config)

        # Media links
        media_links = [
            MediaLink(
                type="Telegram", label="@mytelegram", value="https://t.me/mytelegram"
            ),
            MediaLink(
                type="GitHub",
                label="github.com/myuser",
                value="https://github.com/myuser",
            ),
            MediaLink(type="Email", label="me@example.com", value="me@example.com"),
        ]
        session.add_all(media_links)

        # Vinyl records
        vinyl_records = [
            VinylRecord(
                artist="Daft Punk",
                title="Random Access Memories",
                year=2013,
                genres=["Electronic"],
            ),
            VinylRecord(
                artist="Radiohead",
                title="In Rainbows",
                year=2007,
                genres=["Rock", "Ambient"],
            ),
            VinylRecord(
                artist="Nirvana", title="Nevermind", year=1991, genres=["Rock"]
            ),
            VinylRecord(
                artist="Nujabes",
                title="Modal Soul",
                year=2005,
                genres=["Hip-Hop", "Jazz"],
            ),
            VinylRecord(
                artist="Miles Davis", title="Kind of Blue", year=1959, genres=["Jazz"]
            ),
            VinylRecord(
                artist="Aphex Twin",
                title="Selected Ambient Works 85–92",
                year=1992,
                genres=["Ambient", "Electronic"],
            ),
        ]
        session.add_all(vinyl_records)

        # Books
        books = [
            Book(
                title="Dune",
                author="Frank Herbert",
                genre="Sci‑Fi",
                language="EN",
                format="Hardcover",
            ),
            Book(
                title="Neuromancer",
                author="William Gibson",
                genre="Sci‑Fi",
                language="EN",
                format="Paperback",
            ),
            Book(
                title="Thinking, Fast and Slow",
                author="Daniel Kahneman",
                genre="Non‑fiction",
                language="EN",
                format="Paperback",
            ),
            Book(
                title="The Design of Everyday Things",
                author="Don Norman",
                genre="Design",
                language="EN",
                format="Hardcover",
            ),
            Book(
                title="Designing Data‑Intensive Applications",
                author="Martin Kleppmann",
                genre="Computing",
                language="EN",
                format="Hardcover",
            ),
        ]
        session.add_all(books)

        # Coffee brands and coffees
        brand1 = CoffeeBrand(name="April Coffee")
        brand2 = CoffeeBrand(name="Tim Wendelboe")
        brand3 = CoffeeBrand(name="Friedhats")
        session.add_all([brand1, brand2, brand3])
        await session.flush()  # Get IDs

        coffee1 = Coffee(
            brand_id=brand1.id, name="Ethiopia Guji", region="Guji", processing="Washed"
        )
        coffee2 = Coffee(
            brand_id=brand2.id,
            name="Colombia Huila",
            region="Huila",
            processing="Natural",
        )
        coffee3 = Coffee(
            brand_id=brand3.id, name="Kenya Nyeri", region="Nyeri", processing="Washed"
        )
        session.add_all([coffee1, coffee2, coffee3])
        await session.flush()

        # Coffee reviews
        reviews = [
            CoffeeReview(
                coffee_id=coffee1.id,
                method="Filter",
                rating=9.0,
                notes="bergamot, jasmine, clean finish",
            ),
            CoffeeReview(
                coffee_id=coffee1.id,
                method="Espresso",
                rating=8.4,
                notes="citrus, floral, slightly sharp",
            ),
            CoffeeReview(
                coffee_id=coffee1.id,
                method="Cappuccino",
                rating=8.6,
                notes="sweet, tea-like",
            ),
            CoffeeReview(
                coffee_id=coffee2.id,
                method="Filter",
                rating=7.6,
                notes="cherry, cacao, heavier body",
            ),
            CoffeeReview(
                coffee_id=coffee2.id,
                method="Espresso",
                rating=7.9,
                notes="chocolate, red fruits",
            ),
            CoffeeReview(
                coffee_id=coffee3.id,
                method="Filter",
                rating=8.8,
                notes="blackcurrant, bright acidity",
            ),
            CoffeeReview(
                coffee_id=coffee3.id,
                method="Espresso",
                rating=8.1,
                notes="berry, syrupy",
            ),
        ]
        session.add_all(reviews)

        # Figures
        figures = [
            Figure(name="Nendoroid Example 01", brand="Good Smile"),
            Figure(name="BE@RBRICK Example 100%", brand="Medicom"),
            Figure(name="Figure Example 03", brand="Bandai"),
            Figure(name="Figure Example 04", brand="Kotobukiya"),
        ]
        session.add_all(figures)

        # Projects
        projects = [
            Project(
                name="awesome-tooling",
                description="Небольшие утилиты для автоматизации личных задач.",
                tags=["python", "cli"],
            ),
            Project(
                name="data-viz-notes",
                description="Коллекция заметок и примеров визуализации данных.",
                tags=["viz", "notebooks"],
            ),
            Project(
                name="infra-sandbox",
                description="Песочница под инфраструктуру в облаке (прототипы).",
                tags=["cloud", "iac"],
            ),
        ]
        session.add_all(projects)

        # Publications
        publications = [
            Publication(
                title="Research Paper Example 01",
                venue="Workshop",
                year=2024,
                url="https://example.com",
            ),
            Publication(
                title="Research Paper Example 02",
                venue="Conference",
                year=2023,
                url="https://example.com",
            ),
        ]
        session.add_all(publications)

        # Infographics
        infographics = [
            Infographic(topic="Networks", title="Infographic Example 01"),
            Infographic(topic="ML", title="Infographic Example 02"),
            Infographic(topic="Product", title="Infographic Example 03"),
        ]
        session.add_all(infographics)

        # Plants
        plants = [
            Plant(
                family="Araceae",
                genus="Monstera",
                species="deliciosa",
                common_name="Monstera",
            ),
            Plant(
                family="Cactaceae",
                genus="Mammillaria",
                species="elongata",
                common_name="Mammillaria",
            ),
            Plant(
                family="Moraceae",
                genus="Ficus",
                species="elastica",
                common_name="Rubber plant",
            ),
        ]
        session.add_all(plants)

        await session.commit()
        print("Database seeded successfully!")


async def main():
    await create_tables()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
