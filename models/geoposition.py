from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Geoposition(Base):
    __tablename__ = 'geopositions'
    
    geopos_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship("User", back_populates="geopositions")