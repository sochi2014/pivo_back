from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.level_scheme import LevelSchema


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    level_id: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True


class UserReturnSchema(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str]
    phone_number: Optional[str]
    level: LevelSchema

    class Config:
        orm_mode = True
        from_attributes = True
