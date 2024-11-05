from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class TypeOfPlace(Base):
    __tablename__ = 'type_of_places'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
