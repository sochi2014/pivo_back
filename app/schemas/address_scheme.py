from pydantic import BaseModel, condecimal


class AddressOut(BaseModel):
    id: int
    latitude: condecimal(max_digits=10, decimal_places=7)
    longitude: condecimal(max_digits=10, decimal_places=7)
    country: str
    city: str
    street: str
    house: str

    class Config:
        orm_mode = True
