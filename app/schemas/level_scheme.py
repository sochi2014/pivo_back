from pydantic import BaseModel
from typing import Optional


class LevelSchema(BaseModel):
    id: int
    level_name: str
    icon: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True