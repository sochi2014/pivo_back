import pathlib
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.beer_crud import get_beer, get_all_beers, get_filtered_beers
from app.dependencies import get_db
from app.schemas.beer_schemas import BeerOut
from models import Beer, TypeOfBeer, BeerColor

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


def convert_beer_to_beerout(beer: Beer, db: Session) -> BeerOut:
    type_name = db.query(TypeOfBeer.name).filter(
        TypeOfBeer.id == beer.type_id).scalar()

    color_name = db.query(BeerColor.name).filter(
        BeerColor.id == beer.color_id).scalar() if beer.color_id else None

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
        color_name=color_name
    )


@router.get("/filter", response_model=List[BeerOut])
def filter_beers(
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
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 10
):
    beers = get_filtered_beers(
        db=db,
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
        offset=offset,
        limit=limit
    )
    if not beers:
        raise HTTPException(
            status_code=404, detail="No beers found with the given filters")

    return [convert_beer_to_beerout(beer, db) for beer in beers]


@router.get("", response_model=List[BeerOut])
def read_beers(
    offset: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = 'asc',
    db: Session = Depends(get_db)
):
    beers = get_all_beers(skip=offset, limit=limit, db=db,
                          sort_by=sort_by, order=order)

    if not beers:
        raise HTTPException(status_code=404, detail="No beers found")

    return [convert_beer_to_beerout(beer, db) for beer in beers]


@router.get("/{beer_id}", response_model=BeerOut)
def read_beer(beer_id: int, db: Session = Depends(get_db)):
    beer = db.query(Beer).filter(Beer.id == beer_id).first()
    if beer is None:
        raise HTTPException(status_code=404, detail=f"Beer with id {
                            beer_id} not found")

    return convert_beer_to_beerout(beer, db)
