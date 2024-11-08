

from pydantic import BaseModel
from typing import Optional
from app.schemas.address_scheme import AddressBase


class PlaceCreate(BaseModel):
    name: str
    address_id: int
    type_place_id: int
    phone_number: Optional[str] = None


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    address_id: Optional[int] = None
    type_place_id: Optional[int] = None
    phone_number: Optional[str] = None


class PlaceOut(BaseModel):
    id: int
    name: str
    address_id: int
    type_place_id: int
    phone_number: Optional[str] = None
    address_id: Optional[int] = None
    address: Optional[AddressBase]
    rating: Optional[int] = None

    class Config:
        from_attributes = True
