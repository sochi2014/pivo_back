import pathlib
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import config
from app.crud.test_crud import get_test_db, get_tests_db
from app.dependencies import get_db
from app.schemas.test_scheme import TestOut

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.get("", response_model=List[TestOut])
def read_tests(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tests_db(db, offset=offset, limit=limit)


@router.get("/{test_id}", response_model=TestOut)
def read_test(test_id: int, db: Session = Depends(get_db)):
    db_object = get_test_db(db, test_id=test_id)
    if db_object is None:
        raise HTTPException(status_code=404, detail=f"Object with id {test_id} not found")
    return db_object


