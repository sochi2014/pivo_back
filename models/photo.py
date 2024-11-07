from enum import Enum

from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base



class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_url = Column(String(255), nullable=True)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=True, index=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'), nullable=True, index=True)
    beer_id = Column(Integer, ForeignKey('beers.id'), nullable=True, index=True)

    place = relationship('Place', back_populates='photos')
    feedback = relationship('Feedback', back_populates='photos')
    beer = relationship('Beer', back_populates='photos')
