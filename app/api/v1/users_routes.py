from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.user_crud import get_current_user, update_current_user
from app.schemas.user_scheme import UserUpdate, UserOut
from typing import Annotated
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=UserOut)
def get_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
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


@router.put("/me", response_model=UserOut)
def update_me(
    user_update: UserUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    """
    Обновляет данные текущего аутентифицированного пользователя.
    """
    current_user = get_current_user(token, db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user not authenticated"
        )

    updated_user = update_current_user(
        db=db, user=current_user, user_update=user_update
    )

    return updated_user
