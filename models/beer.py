from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from app.database import Base


class Beer(Base):
    __tablename__ = 'beers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    brand = Column(String(45), nullable=False)
    description = Column(String(250))
    photo = Column(String(100))
    alc_degree = Column(DECIMAL(2, 2), nullable=False)
    type_id = Column(Integer, ForeignKey('type_of_beers.id'), nullable=False)

    type = relationship('TypeOfBeer')
    places = relationship('Place', secondary='beers_places', back_populates='beers')
