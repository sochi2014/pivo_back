from sqlalchemy import Column, Integer, String, Text, DECIMAL
from app.database import Base


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    country = Column(String(255), index=True)
    city = Column(String(255), index=True)
    street = Column(String(255), index=True)
    house = Column(String(20), index=True)
