from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
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


def update_place(db: Session, place_id: int, place_data: PlaceUpdate) -> Place:
    place = get_place(db, place_id)
    if place_data.name is not None:
        place.name = place_data.name
    if place_data.address_id is not None:
        place.address_id = place_data.address_id
    if place_data.type_place_id is not None:
        place.type_place_id = place_data.type_place_id
    if place_data.phone_number is not None:
        place.phone_number = place_data.phone_number

    db.commit()
    db.refresh(place)
    return place


def delete_place(db: Session, place_id: int) -> Place:
    place = get_place(db, place_id)
    db.delete(place)
    db.commit()
    return place
