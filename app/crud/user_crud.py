from models.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db


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
