from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True)
    ratings = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    beer_id = Column(Integer, ForeignKey('beers.id'), nullable=True, index=True)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=True, index=True)
    type_feedback = Column(String(10), nullable=False)
    photo_url = Column(String(255), nullable=True)

    user = relationship('User', back_populates='feedbacks')
    beer = relationship('Beer', back_populates='feedbacks')
    place = relationship('Place', back_populates='feedbacks')
    photos = relationship('Photo', back_populates='feedback')

    __table_args__ = (
        CheckConstraint("type_feedback IN ('beer', 'place')", name="check_type_feedback"),
    )
