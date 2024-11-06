from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


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


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    register_at: datetime.datetime

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
