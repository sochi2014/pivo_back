# app/schemas.py
from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class GeopositionBase(BaseModel):
    user_id: int
    latitude: condecimal(max_digits=10, decimal_places=7)
    longitude: condecimal(max_digits=10, decimal_places=7)

class GeopositionCreate(GeopositionBase):
    pass

class GeopositionUpdate(BaseModel):
    latitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None
    longitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None

class GeopositionOut(GeopositionBase):
    geopos_id: int
    updated_at: datetime

    class Config:
        orm_mode = True
