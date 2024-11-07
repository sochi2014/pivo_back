import json
from typing import Optional, List

from pydantic import BaseModel, model_validator


class FilterValues(BaseModel):
    name: str
    key: str
    values: List[str]


class FilterRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None


class FiltersResponse(BaseModel):
    type: List[FilterValues]
    color: List[FilterValues]
    alc_degree: FilterRange
    ibu: FilterRange
    og: FilterRange
    fg: FilterRange
