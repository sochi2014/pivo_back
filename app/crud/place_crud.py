from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session, joinedload, aliased
from fastapi import HTTPException
from typing import List, Optional

from models import TypeOfPlace, Address, Feedback
from models.place import Place
from app.schemas.place_scheme import PlaceCreate, PlaceUpdate


def create_place(db: Session, place: PlaceCreate) -> Place:
    db_place = Place(
        name=place.name,
        address_id=place.address_id,
        type_place_id=place.type_place_id,
        phone_number=place.phone_number
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


def get_place(db: Session, place_id: int) -> Place:
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


def get_places(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name_filter: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        sort_by: Optional[str] = None,
        order: str = 'asc'
) -> List[Place]:

    VALID_SORT_FIELDS = ['name', 'rating']

    query = db.query(Place).options(
        joinedload(Place.type_place),
        joinedload(Place.address)
    )

    if name_filter:
        query = query.filter(Place.name.ilike(f"%{name_filter}%"))

    if min_rating is not None or max_rating is not None:
        feedback_alias = aliased(Feedback)
        query = query.outerjoin(feedback_alias, Place.id == feedback_alias.place_id).group_by(Place.id)

        if min_rating is not None:
            query = query.having(func.avg(feedback_alias.ratings) >= min_rating)
        if max_rating is not None:
            query = query.having(func.avg(feedback_alias.ratings) <= max_rating)

    column = getattr(Place, sort_by, None)

    if column is not None:
        query = query.order_by(asc(column) if order == 'asc' else desc(column))
    elif sort_by == 'rating':
        feedback_alias = aliased(Feedback)
        query = query.outerjoin(feedback_alias, Place.id == feedback_alias.place_id).group_by(Place.id).order_by(
            asc(func.avg(feedback_alias.ratings)) if order == 'asc' else desc(func.avg(feedback_alias.ratings))
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by value, choose from: {', '.join(VALID_SORT_FIELDS)}"
        )

    return query.offset(skip).limit(limit).all()
