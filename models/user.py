from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_id = Column(Integer, ForeignKey(
        "levels.id"), nullable=False, default=1)
    username = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String, nullable=True)
    register_at = Column(DateTime, default=datetime.datetime.utcnow)

    level = relationship("Level", back_populates="users")
    auth_codes = relationship("AuthCode", back_populates="user")
