from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.coffee import Coffee, CoffeeBrand, CoffeeReview
from app.repositories.base import BaseRepository


class CoffeeBrandRepository(BaseRepository[CoffeeBrand]):
    def __init__(self, db):
        super().__init__(CoffeeBrand, db)


class CoffeeRepository(BaseRepository[Coffee]):
    def __init__(self, db):
        super().__init__(Coffee, db)

    async def list_with_reviews(self) -> list[Coffee]:
        query = select(Coffee).options(
            selectinload(Coffee.reviews), selectinload(Coffee.brand)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class CoffeeReviewRepository(BaseRepository[CoffeeReview]):
    def __init__(self, db):
        super().__init__(CoffeeReview, db)
