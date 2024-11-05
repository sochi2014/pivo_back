from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False, index=True)
    type_place_id = Column(Integer, ForeignKey('type_of_places.id'), nullable=False, index=True)
    phone_number = Column(String(20))

    address = relationship('Address')
    type_place = relationship('TypeOfPlace')
