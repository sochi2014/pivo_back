from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Table
from sqlalchemy.orm import relationship

from app.database import Base


beers_places = Table(
    'beers_places', Base.metadata,
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('beer_id', Integer, ForeignKey('beers.id'), primary_key=True)
)
