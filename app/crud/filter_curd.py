from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from models import Beer, TypeOfBeer, BeerColor
from app.schemas.filters_scheme import FiltersResponse, FilterValues, FilterRange


def get_filter_values(db: Session) -> FiltersResponse:
    type_values = db.query(TypeOfBeer.name).distinct().all()
    color_values = db.query(BeerColor.name).distinct().all()

    alc_degree_range = db.query(func.min(Beer.alc_degree), func.max(Beer.alc_degree)).first()
    ibu_range = db.query(func.min(Beer.ibu), func.max(Beer.ibu)).first()
    og_range = db.query(func.min(Beer.og), func.max(Beer.og)).first()
    fg_range = db.query(func.min(Beer.fg), func.max(Beer.fg)).first()

    return FiltersResponse(
        type=[FilterValues(name="тип", key="type", values=[val[0] for val in type_values])],
        color=[FilterValues(name="цвет", key="color", values=[val[0] for val in color_values])],
        alc_degree=FilterRange(min=alc_degree_range[0], max=alc_degree_range[1]),
        ibu=FilterRange(min=ibu_range[0], max=ibu_range[1]),
        og=FilterRange(min=og_range[0], max=og_range[1]),
        fg=FilterRange(min=fg_range[0], max=fg_range[1]),
    )
