from sqlalchemy import Column, Integer, String, Text, DECIMAL
from app.database import Base


class BeerColor(Base):
    __tablename__ = 'beer_colors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    srm = Column(DECIMAL(4, 2))  # Стандартный метод SRM
    ebc = Column(DECIMAL(4, 2))  # Европейская шкала EBC
