from pydantic import BaseModel
from typing import Optional


class UserGeoOut(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    phone_number: Optional[str] = None 

    class Config:
        orm_mode = True
