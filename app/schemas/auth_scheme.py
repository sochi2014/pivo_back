from pydantic import BaseModel, EmailStr
from typing import Optional


class RegistrationSchema(BaseModel):
    email: EmailStr
    username: str
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None


class AuthCodeSchema(BaseModel):
    email: EmailStr
    code: Optional[str] = None
