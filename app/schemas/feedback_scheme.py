from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

from app.schemas.photo_scheme import PhotoOut


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
    user_id: int
    beer_id: Optional[int]
    place_id: Optional[int]
    type_feedback: str
    photos: List[PhotoOut]

    class Config:
        from_attributes = True
