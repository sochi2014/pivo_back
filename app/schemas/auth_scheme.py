from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.geoposition_sheme import GeopositionOut
class RegistrationSchema(BaseModel):
    email: EmailStr
    username: str
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None


class AuthCodeSchema(BaseModel):
    email: EmailStr
    code: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    geopositions: List[GeopositionOut] = []

    class Config:
        orm_mode = True
