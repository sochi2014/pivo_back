from models.user import User
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.token_crud import decode_access_token
from app.schemas.user_scheme import UserUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(email: str, username: str = None, avatar_url: str = None, db: Session = Depends(get_db)) -> User:
    new_user = User(
        email=email,
        username=username,
        avatar_url=avatar_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not autorized",
        )
    return user


def update_current_user(
    db: Session,
    user: User,
    user_update: UserUpdate
) -> User:
    """
    Обновляет данные текущего пользователя.

    :param db: Сессия базы данных
    :param user: Объект текущего пользователя
    :param user_update: Данные для обновления
    :return: Обновленный объект пользователя
    """
    update_data = user_update.dict(exclude_unset=True)

    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"]).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already used",
            )

    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
