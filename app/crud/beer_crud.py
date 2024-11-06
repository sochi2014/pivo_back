from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import List, Optional, Tuple, Union, Dict, Any

from models.beer import Beer
from app.dependencies import get_db


def get_beer(beer_id: int, db: Session = Depends(get_db)) -> Optional[Beer]:
    return db.query(Beer).filter(Beer.id == beer_id).first()


def get_all_beers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Beer]:
    return db.query(Beer).offset(skip).limit(limit).all()

def get_filtered_beers(
    db: Session,
    type: Optional[str] = None,
    color: Optional[str] = None,
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
