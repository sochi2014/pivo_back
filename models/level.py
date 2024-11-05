from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True,
                index=True, autoincrement=True)
    level_name = Column(String(45), nullable=False)
    icon = Column(String(200), nullable=True)

    users = relationship("User", back_populates="level")
