from sqlalchemy.orm import Session
from models import Feedback, Level, User
from fastapi import HTTPException


def update_user_level(user_id: int, db: Session):

    feedback_count = db.query(Feedback).filter(Feedback.user_id == user_id).count()

    MAX_LEVEL = 5

    new_level_id = min((feedback_count // 10) + 1, MAX_LEVEL)

    new_level = db.query(Level).filter(Level.id == new_level_id).first() 
    if not new_level:
        raise HTTPException(status_code=404, detail="Level not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.level_id = new_level.id
    db.commit()

    return user