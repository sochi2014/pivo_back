from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from app.schemas.user_scheme import UserReturnSchema
from app.schemas.photo_scheme import PhotoOut
from app.schemas.beer_schemas import BeerOut
from app.schemas.place_scheme import PlaceOut


class FeedbackCreate(BaseModel):
    text: Optional[str]
    ratings: int
    user_id: int
    beer_id: Optional[int] = None
    place_id: Optional[int] = None
    type_feedback: str
    photo_urls: List[str]


class FeedbackOut(BaseModel):
    id: int
    text: Optional[str]
    ratings: int
    place: Optional[PlaceOut]
    type_feedback: str
    photos: List[PhotoOut]
    beer: Optional[BeerOut]
    user: UserReturnSchema

    class Config:
        from_attributes = True
