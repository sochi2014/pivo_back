from sqlalchemy import asc, desc, func, text
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException
from typing import List, Optional, Tuple, Union, Dict, Any

from models import Feedback, BeerColor, TypeOfBeer
from models.beer import Beer
from app.dependencies import get_db


def get_beer(beer_id: int, db: Session = Depends(get_db)) -> Optional[Beer]:
    return db.query(Beer).filter(Beer.id == beer_id).first()


def get_beers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = 'asc',
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
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None
) -> List[Beer]:

    query = db.query(Beer).options(
        joinedload(Beer.type), joinedload(Beer.color)
    )

    if type:
        query = query.join(Beer.type).filter(Beer.type.has(TypeOfBeer.name.ilike(f"%{type}%")))
    if color:
        query = query.join(Beer.color).filter(Beer.color.has(BeerColor.name.ilike(f"%{color}%")))
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

    if min_rating is not None or max_rating is not None:
        query = query.outerjoin(Feedback).group_by(Beer.id)
        if min_rating is not None:
            query = query.having(func.avg(Feedback.ratings) >= min_rating)
        if max_rating is not None:
            query = query.having(func.avg(Feedback.ratings) <= max_rating)

    if sort_by:
        valid_sort_fields = ['rating', 'name', 'alc_degree']
        if sort_by not in valid_sort_fields:
            raise HTTPException(status_code=400,
                                detail=f"Invalid sort_by value, choose from: {', '.join(valid_sort_fields)}")

        column = getattr(Beer, sort_by, None)
        if column is not None:
            query = query.order_by(asc(column) if order == 'asc' else desc(column))
        elif sort_by == 'rating':
            query = query.outerjoin(Feedback).group_by(Beer.id).order_by(
                asc(func.avg(Feedback.ratings)) if order == 'asc' else desc(func.avg(Feedback.ratings))
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid order value")

    return query.offset(skip).limit(limit).all()
