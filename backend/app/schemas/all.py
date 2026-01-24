from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class About(BaseModel):
    bio: str

    model_config = ConfigDict(from_attributes=True)


class VinylRecord(BaseModel):
    id: str  # UUID as string to match frontend
    artist: str
    title: str
    year: Optional[int] = None
    genres: List[str]

    model_config = ConfigDict(from_attributes=True)


class Book(BaseModel):
    id: str  # UUID as string
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CoffeeBrand(BaseModel):
    id: str  # UUID as string
    name: str

    model_config = ConfigDict(from_attributes=True)


class CoffeeReview(BaseModel):
    method: str
    rating: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Coffee(BaseModel):
    id: str  # UUID as string
    brandId: str  # CamelCase to match frontend
    name: str
    region: Optional[str] = None
    processing: Optional[str] = None
    reviews: List[CoffeeReview]

    model_config = ConfigDict(from_attributes=True)


class Figure(BaseModel):
    id: str  # UUID as string
    name: str
    brand: str

    model_config = ConfigDict(from_attributes=True)


class Project(BaseModel):
    id: str  # UUID as string
    name: str
    desc: str  # CamelCase to match frontend
    tags: List[str]

    model_config = ConfigDict(from_attributes=True)


class Publication(BaseModel):
    id: str  # UUID as string
    title: str
    venue: Optional[str] = None
    year: Optional[int] = None
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Infographic(BaseModel):
    id: str  # UUID as string
    topic: Optional[str] = None
    title: str

    model_config = ConfigDict(from_attributes=True)


class Plant(BaseModel):
    id: str  # UUID as string
    family: Optional[str] = None
    genus: Optional[str] = None
    species: Optional[str] = None
    commonName: Optional[str] = None  # CamelCase to match frontend

    model_config = ConfigDict(from_attributes=True)


class MediaLink(BaseModel):
    type: str
    label: Optional[str] = None
    value: str

    model_config = ConfigDict(from_attributes=True)


class Media(BaseModel):
    externalWishUrl: str  # CamelCase to match frontend
    links: List[MediaLink]

    model_config = ConfigDict(from_attributes=True)


class AllDataResponse(BaseModel):
    about: About
    vinylGenres: List[str]  # CamelCase to match frontend
    vinyl: List[VinylRecord]
    books: List[Book]
    coffeeBrands: List[CoffeeBrand]
    coffee: List[Coffee]
    figures: List[Figure]
    projects: List[Project]
    publications: List[Publication]
    infographics: List[Infographic]
    plants: List[Plant]
    media: Media

    model_config = ConfigDict(from_attributes=True)
