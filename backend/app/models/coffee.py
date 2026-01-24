from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common import Base, UUIDMixin


class CoffeeBrand(Base, UUIDMixin):
    __tablename__ = "coffee_brands"

    name = Column(String, nullable=False, unique=True)

    coffees = relationship("Coffee", back_populates="brand")


class Coffee(Base, UUIDMixin):
    __tablename__ = "coffees"

    brand_id = Column(
        UUID(as_uuid=True), ForeignKey("coffee_brands.id"), nullable=False
    )
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)
    processing = Column(String, nullable=True)

    brand = relationship("CoffeeBrand", back_populates="coffees")
    reviews = relationship(
        "CoffeeReview", back_populates="coffee", cascade="all, delete-orphan"
    )


class CoffeeReview(Base, UUIDMixin):
    __tablename__ = "coffee_reviews"

    coffee_id = Column(UUID(as_uuid=True), ForeignKey("coffees.id"), nullable=False)
    method = Column(String, nullable=False)  # espresso, cappuccino, filter, etc.
    rating = Column(Float, nullable=True)  # 0-10 scale
    notes = Column(String, nullable=True)

    coffee = relationship("Coffee", back_populates="reviews")
