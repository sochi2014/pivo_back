from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class TypeOfBeer(Base):
    __tablename__ = 'type_of_beers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), index=True)
    description = Column(String(200))
