from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class TypeOfPlace(Base):
    __tablename__ = 'type_of_places'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))

    places = relationship('Place', back_populates='type_place')
