from typing import List, Optional

from sqlalchemy.orm import Session
from models.test_model import TestModel


def get_test_db(db: Session, test_id: int) -> TestModel:
    return db.query(TestModel).filter(TestModel.id == test_id).first()


def get_tests_db(db: Session, offset: int = 0, limit: int = 10) -> List[TestModel]:
    return db.query(TestModel).offset(offset).limit(limit).all()
