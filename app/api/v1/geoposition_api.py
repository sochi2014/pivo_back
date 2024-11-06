from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.schemas.user_schemas import AuthCodeSchema, RegistrationSchema
from app.dependencies import get_db
from models.auth_code import AuthCode
from models.user import User
from fastapi.responses import JSONResponse
from app.utils.base_utils import send_email, get_user_by_email
from app.utils.auth_utils import (verify_auth_code_and_generate_tokens,
                                  send_auth_code, generate_auth_code)
from app.crud.token_crud import revoke_refresh_token, verify_refresh_token, create_access_token
from pydantic import ValidationError
from app.schemas.geoposition_sheme import GeopositionOut, GeopositionCreate, GeopositionUpdate
from app.schemas.user_schemas import UserOut
import datetime
import pathlib
from typing import List

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)

@router.post("/geopositions/", response_model=GeopositionOut, status_code=status.HTTP_201_CREATED)
def create_geoposition(geoposition: GeopositionCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == geoposition.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.create_geoposition(db=db, geoposition=geoposition)


@router.get("/geopositions/{geopos_id}", response_model=GeopositionOut)
def read_geoposition(geopos_id: int, db: Session = Depends(get_db)):
    geoposition = crud.get_geoposition(db, geopos_id=geopos_id)
    if geoposition is None:
        raise HTTPException(status_code=404, detail="Geoposition not found")
    return geoposition


@router.put("/geopositions/{geopos_id}", response_model=GeopositionOut)
def update_geoposition(geopos_id: int, geoposition: GeopositionUpdate, db: Session = Depends(get_db)):
    updated_geoposition = crud.update_geoposition(db, geopos_id=geopos_id, geoposition=geoposition)
    if updated_geoposition is None:
        raise HTTPException(status_code=404, detail="Geoposition not found")
    return updated_geoposition

@router.delete("/geopositions/{geopos_id}", response_model=GeopositionOut)
def delete_geoposition(geopos_id: int, db: Session = Depends(get_db)):
    deleted_geoposition = crud.delete_geoposition(db, geopos_id=geopos_id)
    if deleted_geoposition is None:
        raise HTTPException(status_code=404, detail="Geoposition not found")
    return deleted_geoposition

@router.get("/users/nearby", response_model=List[UserOut])
def find_users_nearby(
    current_lat: float,
    current_lon: float,
    db: Session = Depends(get_db)
):
    radius_km = 1.0

    lat_change = radius_km / 111.0
    lon_change = radius_km / (111.0 * math.cos(math.radians(current_lat)))
    min_lat = current_lat - lat_change
    max_lat = current_lat + lat_change
    min_lon = current_lon - lon_change
    max_lon = current_lon + lon_change

    distance = haversine_formula(current_lat, current_lon, Geoposition.latitude, Geoposition.longitude)

    users = db.query(User).join(Geoposition).filter(
        Geoposition.latitude.between(min_lat, max_lat),
        Geoposition.longitude.between(min_lon, max_lon),
        distance <= radius_km
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found nearby")

    return users
