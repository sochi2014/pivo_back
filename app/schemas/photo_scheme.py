from pydantic import BaseModel
from typing import Optional, List


class PhotoOut(BaseModel):
    id: int
    photo_url: str

    class Config:
        from_attributes = True


class PhotoIn(BaseModel):
    photo_url: str
    feedback_id: int
    beer_id: Optional[int] = None
    place_id: Optional[int] = None
