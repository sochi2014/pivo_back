import pathlib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.filter_curd import get_filter_values
from app.dependencies import get_db
from app.schemas.filters_scheme import FiltersResponse

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.get("/beer", response_model=FiltersResponse)
def read_filters(db: Session = Depends(get_db)):
    return get_filter_values(db)
