from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import List, Optional, Tuple, Union, Dict, Any

from models.beer import Beer
from app.dependencies import get_db
from sqlalchemy import asc, desc


def get_beer(beer_id: int, db: Session = Depends(get_db)) -> Optional[Beer]:
    return db.query(Beer).filter(Beer.id == beer_id).first()


def get_all_beers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    sort_by: Optional[str] = None,
    order: str = 'asc'
) -> List[Beer]:
    query = db.query(Beer)

    if sort_by:
        valid_sort_fields = ['rating', 'name', 'alc_degree']
        if sort_by not in valid_sort_fields:
            raise HTTPException(
                status_code=400, detail="Invalid sort_by value")

        column = getattr(Beer, sort_by)
        if order == 'asc':
            query = query.order_by(asc(column))
        elif order == 'desc':
            query = query.order_by(desc(column))
        else:
            raise HTTPException(status_code=400, detail="Invalid order value")

    return query.offset(skip).limit(limit).all()


def get_filtered_beers(
    db: Session,
    type: Optional[str] = None,
    color: Optional[str] = None,
    brand: Optional[str] = None,
    name: Optional[str] = None,
    min_alc_degree: Optional[float] = None,
    max_alc_degree: Optional[float] = None,
    min_ibu: Optional[int] = None,
    max_ibu: Optional[int] = None,
    min_og: Optional[float] = None,
    max_og: Optional[float] = None,
    min_fg: Optional[float] = None,
    max_fg: Optional[float] = None,
    offset: int = 0,
    limit: int = 10
) -> List[Beer]:
    query = db.query(Beer)
    if type:
        query = query.join(Beer.type).filter(Beer.type.has(name=type))
    if color:
        query = query.join(Beer.color).filter(Beer.color.has(name=color))
    if brand:
        query = query.filter(Beer.brand.ilike(f"%{brand}%"))
    if name:
        query = query.filter(Beer.name.ilike(f"%{name}%"))
    if min_alc_degree is not None:
        query = query.filter(Beer.alc_degree >= min_alc_degree)
    if max_alc_degree is not None:
        query = query.filter(Beer.alc_degree <= max_alc_degree)
    if min_ibu is not None:
        query = query.filter(Beer.ibu >= min_ibu)
    if max_ibu is not None:
        query = query.filter(Beer.ibu <= max_ibu)
    if min_og is not None:
        query = query.filter(Beer.og >= min_og)
    if max_og is not None:
        query = query.filter(Beer.og <= max_og)
    if min_fg is not None:
        query = query.filter(Beer.fg >= min_fg)
    if max_fg is not None:
        query = query.filter(Beer.fg <= max_fg)
    return query.offset(offset).limit(limit).all()
