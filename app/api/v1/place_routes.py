from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.place_crud import create_place, get_place, get_places
from app.schemas.place_scheme import PlaceCreate, PlaceUpdate, PlaceOut
from app.dependencies import get_db
from models import Feedback
from models.place import Place
from app.schemas.address_scheme import AddressOut
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)

def convert_place_to_placeout(place: Place, db: Session) -> PlaceOut:
    average_rating = db.query(func.avg(Feedback.ratings)).filter(Feedback.place_id == place.id).scalar()
    average_rating = round(average_rating) if average_rating is not None else None

    return PlaceOut(
        id=place.id,
        name=place.name,
        type_place_id=place.type_place_id,
        phone_number=place.phone_number,
        address=AddressOut.from_orm(place.address) if place.address else None,
        rating=average_rating
    )


@router.get("", response_model=List[PlaceOut])
def read_all_places(
    offset: int = 0,
    limit: int = 10,
    name_filter: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: str = 'asc',
    db: Session = Depends(get_db)
):
    places = get_places(
        db=db,
        skip=offset,
        limit=limit,
        name_filter=name_filter,
        min_rating=min_rating,
        max_rating=max_rating,
        sort_by=sort_by,
        order=order
    )
    if not places:
        raise HTTPException(status_code=404, detail="No places found")

    return [convert_place_to_placeout(place, db) for place in places]


# @router.get("/", response_model=List[PlaceOut])
# def read_places(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     query = db.query(Place).offset(offset).limit(limit)
#
#     places = query.all()
#
#     if not places:
#         raise HTTPException(status_code=404, detail="No places found")
#
#     return [
#         PlaceOut(
#             id=place.id,
#             name=place.name,
#             type_place_id=place.type_place_id,
#             phone_number=place.phone_number,
#             address=AddressOut.from_orm(
#                 place.address) if place.address else None
#         )
#         for place in places
#     ]


# @router.put("/{place_id}", response_model=PlaceOut)
# def update_place_route(place_id: int, place_data: PlaceUpdate, db: Session = Depends(get_db)):
#     return update_place(db=db, place_id=place_id, place_data=place_data)


# @router.delete("/{place_id}", response_model=dict)
# def delete_place_route(place_id: int, db: Session = Depends(get_db)):
#     delete_place(db=db, place_id=place_id)
#     return {"message": "Place deleted"}


@router.get("/{place_id}", response_model=PlaceOut)
def read_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404,
                            detail=f"Place with id {place_id} not found")

    return PlaceOut(
        id=place.id,
        name=place.name,
        type_place_id=place.type_place_id,
        phone_number=place.phone_number,
        address=AddressOut.from_orm(place.address) if place.address else None
    )
