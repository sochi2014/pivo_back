import json
from typing import Optional

from pydantic import BaseModel, model_validator


class TestBase(BaseModel):
    title: str
    description: Optional[str] = None


class TestCreate(TestBase):
    """
    Schema for creating.
    Validates if the input is a JSON string and converts it to a dictionary.
    """

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class TestUpdate(BaseModel):
    """
    Schema for updating.
    All fields are optional.
    """
    title: Optional[str] = None
    description: Optional[str] = None


class TestOut(TestBase):
    """
    Schema for returning object to user.
    """
    id: int

    class Config:
        from_attributes = True
