import pathlib
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.crud.beer_crud import get_beer, get_beers
from app.dependencies import get_db
from app.schemas.beer_schemas import BeerOut
from models import Beer, TypeOfBeer, BeerColor, Feedback

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


def convert_beer_to_beerout(beer: Beer, db: Session) -> BeerOut:
    type_name = beer.type.name
    color_name = beer.color.name if beer.color_id else None

    average_rating = db.query(func.avg(Feedback.ratings)).filter(Feedback.beer_id == beer.id).scalar()
    average_rating = round(average_rating) if average_rating is not None else None

    return BeerOut(
        id=beer.id,
        name=beer.name,
        brand=beer.brand,
        type_name=type_name,
        alc_degree=beer.alc_degree,
        description=beer.description,
        photo=beer.photo,
        ibu=beer.ibu,
        og=beer.og,
        fg=beer.fg,
        barrel_aged=beer.barrel_aged,
        color_name=color_name,
        rating=average_rating
    )


@router.get("", response_model=List[BeerOut])
def get_all_beers(
    type: Optional[str] = None,
    color: Optional[str] = None,
    brand: Optional[str] = None,
    name: Optional[str] = None,
    min_alc_degree: Optional[float] = Query(None, alias="min_alc"),
    max_alc_degree: Optional[float] = Query(None, alias="max_alc"),
    min_ibu: Optional[int] = None,
    max_ibu: Optional[int] = None,
    min_og: Optional[float] = None,
    max_og: Optional[float] = None,
    min_fg: Optional[float] = None,
    max_fg: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = 'asc',
    db: Session = Depends(get_db)
):
    beers = get_beers(
        db=db,
        skip=offset,
        limit=limit,
        sort_by=sort_by,
        order=order,
        type=type,
        color=color,
        brand=brand,
        name=name,
        min_alc_degree=min_alc_degree,
        max_alc_degree=max_alc_degree,
        min_ibu=min_ibu,
        max_ibu=max_ibu,
        min_og=min_og,
        max_og=max_og,
        min_fg=min_fg,
        max_fg=max_fg,
        min_rating=min_rating,
        max_rating=max_rating
    )
    if not beers:
        raise HTTPException(status_code=404, detail="No beers found with the given filters and parameters")

    return [convert_beer_to_beerout(beer, db) for beer in beers]


@router.get("/{beer_id}", response_model=BeerOut)
def read_beer(beer_id: int, db: Session = Depends(get_db)):
    beer = db.query(Beer).filter(Beer.id == beer_id).first()
    if beer is None:
        raise HTTPException(status_code=404, detail=f"Beer with id {beer_id} not found")

    return convert_beer_to_beerout(beer, db)

