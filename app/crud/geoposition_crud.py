# app/crud.py
from sqlalchemy.orm import Session
from models.geoposition import Geoposition
from schemas.geoposition_sheme import GeopositionCreate

def get_geoposition(db: Session, geopos_id: int):
    return db.query(Geoposition).filter(Geoposition.geopos_id == geopos_id).first()

def get_geopositions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Geoposition).offset(skip).limit(limit).all()

def create_geoposition(db: Session, geoposition: GeopositionCreate):
    db_geoposition = Geoposition(**geoposition.dict())
    db.add(db_geoposition)
    db.commit()
    db.refresh(db_geoposition)
    return db_geoposition

def update_geoposition(db: Session, geopos_id: int, geoposition: schemas.GeopositionUpdate):
    db_geoposition = db.query(Geoposition).filter(Geoposition.geopos_id == geopos_id).first()
    if db_geoposition is None:
        return None
    for var, value in vars(geoposition).items():
        if value is not None:
            setattr(db_geoposition, var, value)
    db.commit()
    db.refresh(db_geoposition)
    return db_geoposition

def delete_geoposition(db: Session, geopos_id: int):
    db_geoposition = db.query(models.Geoposition).filter(models.Geoposition.geopos_id == geopos_id).first()
    if db_geoposition is None:
        return None
    db.delete(db_geoposition)
    db.commit()
    return db_geoposition

import math

def haversine_formula(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками на Земле с использованием формулы Хаверсина.
    
    :param lat1: Широта первой точки в градусах
    :param lon1: Долгота первой точки в градусах
    :param lat2: Широта второй точки в градусах
    :param lon2: Долгота второй точки в градусах
    :return: Расстояние между точками в километрах
    """
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
