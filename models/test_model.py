from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class TestModel(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
