from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class BeerOut(BaseModel):
    id: int
    name: str
    brand: str
    type_name: str
    alc_degree: float
    color_name: Optional[str] = None
    description: Optional[str] = None
    photo: Optional[str] = None
    ibu: Optional[int] = None
    og: Optional[float] = None
    fg: Optional[float] = None
    barrel_aged: Optional[bool] = None
    rating: Optional[int] = None

    class Config:
        from_attributes = True

