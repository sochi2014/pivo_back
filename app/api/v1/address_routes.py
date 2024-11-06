from app.schemas.address_scheme import AddressOut
from models.address import Address
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


def convert_address_to_addressout(address: Address) -> AddressOut:
    return AddressOut(
        id=address.id,
        latitude=address.latitude,
        longitude=address.longitude,
        country=address.country,
        city=address.city,
        street=address.street,
        house=address.house
    )


@router.get("/filter", response_model=List[AddressOut])
def filter_addresses(
        country: Optional[str] = None,
        city: Optional[str] = None,
        street: Optional[str] = None,
        house: Optional[str] = None,
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 10
):
    query = db.query(Address)

    if country:
        query = query.filter(Address.country == country)
    if city:
        query = query.filter(Address.city == city)
    if street:
        query = query.filter(Address.street == street)
    if house:
        query = query.filter(Address.house == house)

    addresses = query.offset(offset).limit(limit).all()

    if not addresses:
        raise HTTPException(
            status_code=404, detail="No addresses found with the given filters")

    return [convert_address_to_addressout(address) for address in addresses]


@router.get("", response_model=List[AddressOut])
def read_addresses(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    addresses = db.query(Address).offset(offset).limit(limit).all()
    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found")
    return [convert_address_to_addressout(address) for address in addresses]


@router.get("/{address_id}", response_model=AddressOut)
def read_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail=f"Address with id {
                            address_id} not found")

    return convert_address_to_addressout(address)
