from models.user import User
from app.database import SessionLocal


def get_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user


def create_user(email: str, username: str = None, avatar_url: str = None) -> User:
    db = SessionLocal()
    new_user = User(
        email=email,
        username=username,
        avatar_url=avatar_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user
