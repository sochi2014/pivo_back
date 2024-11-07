from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.level_scheme import LevelSchema
from models import Level
import pathlib
_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.get("/levels", response_model=List[LevelSchema])
def get_levels(db: Session = Depends(get_db)):
    levels = db.query(Level).all()
    if not levels:
        raise HTTPException(status_code=404, detail="No levels found")
    return levels