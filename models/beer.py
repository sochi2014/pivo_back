from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Boolean
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
    ibu = Column(Integer)  # Международная шкала горечи IBU
    og = Column(DECIMAL(5, 3))  # Исходная плотность OG
    fg = Column(DECIMAL(5, 3))  # Конечная плотность FG
    barrel_aged = Column(Boolean, default=False)  # Выдержка BA

    type_id = Column(Integer, ForeignKey('type_of_beers.id'), nullable=False)
    color_id = Column(Integer, ForeignKey('beer_colors.id'), nullable=True)

    type = relationship('TypeOfBeer')
    color = relationship('BeerColor')
    feedbacks = relationship('Feedback', back_populates='beer')
    photos = relationship('Photo', back_populates='beer')
