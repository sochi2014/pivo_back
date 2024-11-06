from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.user_crud import get_current_user, update_current_user
from app.schemas.user_scheme import UserUpdate, UserReturnSchema
from app.schemas.level_scheme import LevelSchema
from typing import Annotated
from models.level import Level
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=UserReturnSchema)
def get_me(token: str, db: Session = Depends(get_db)):
    """
    Получает данные текущего аутентифицированного пользователя.
    """
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user not authenticated"
        )
    return user


@router.put("/me", response_model=UserReturnSchema)
def update_me(
    user_update: UserUpdate,
    token: str,
    db: Session = Depends(get_db),
):
    """
    Обновляет данные текущего аутентифицированного пользователя, включая уровень и URL аватарки.
    """
    current_user = get_current_user(token, db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user not authenticated"
        )

    if user_update.level_id:
        level = db.query(Level).filter(
            Level.id == user_update.level_id).first()
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specified level not found"
            )
        current_user.level = level

    if user_update.avatar_url:
        current_user.avatar = user_update.avatar_url

    updated_user = update_current_user(
        db=db, user=current_user, user_update=user_update)
    db.commit()
    db.refresh(updated_user)

    return updated_user
