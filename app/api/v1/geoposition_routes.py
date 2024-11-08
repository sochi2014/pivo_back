from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from models.user import User
from app.schemas.geoposition_sheme import GeopositionBase, GeopositionCreate, \
    GeopositionOut, GeopositionUpdate
from app.crud.geoposition_crud import delete_geoposition, create_geoposition
from app.crud.user_crud import get_current_user
from models.geoposition import Geoposition
from app.schemas.usergeo_sheme import UserGeoOut
import pathlib
import math
from datetime import datetime, timedelta
from typing import List

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.post("", response_model=GeopositionOut, status_code=status.HTTP_201_CREATED)
def create_geoposition_endpoint(
    geoposition: GeopositionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_geoposition = current_user.geoposition
    if existing_geoposition is not None:
        delete_geoposition(db, geopos_id=existing_geoposition.id)

    new_geoposition = create_geoposition(
        db=db,
        geoposition=geoposition,
        user_id=current_user.id
    )
    return new_geoposition


@router.get("/users/nearby", response_model=List[UserGeoOut])
def find_users_nearby(
    radius_km: float = 1.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.geoposition:
        raise HTTPException(
            status_code=400, detail="User's location is not set")
    current_lat = float(current_user.geoposition.latitude)
    current_lon = float(current_user.geoposition.longitude)

    lat_change = radius_km / 111.0
    lon_change = radius_km / (111.0 * math.cos(math.radians(current_lat)))

    min_lat = current_lat - lat_change
    max_lat = current_lat + lat_change
    min_lon = current_lon - lon_change
    max_lon = current_lon + lon_change

    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)

    users_in_box = db.query(User).join(Geoposition).filter(
        Geoposition.latitude.between(min_lat, max_lat),
        Geoposition.longitude.between(min_lon, max_lon),
        User.phone_number.isnot(None),
        Geoposition.updated_at >= one_minute_ago
    ).all()

    nearby_users = []
    for user in users_in_box:
        if user.id == current_user.id:
            continue
        user_lat = float(user.geoposition.latitude)
        user_lon = float(user.geoposition.longitude)
        distance = haversine_formula(
            current_lat, current_lon, user_lat, user_lon)
        if distance <= radius_km:
            nearby_users.append(UserGeoOut(
                id=user.id,
                name=user.username,
                latitude=user_lat,
                longitude=user_lon,
                phone_number=user.phone_number
            ))

    if not nearby_users:
        raise HTTPException(status_code=404, detail="No users found nearby")

    return nearby_users


def haversine_formula(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth's surface.

    :param lat1: Latitude of the first point in decimal degrees
    :param lon1: Longitude of the first point in decimal degrees
    :param lat2: Latitude of the second point in decimal degrees
    :param lon2: Longitude of the second point in decimal degrees
    :return: Distance between the two points in kilometers
    """
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
