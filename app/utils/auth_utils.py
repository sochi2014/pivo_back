import datetime
from sqlalchemy.orm import Session
from models.auth_code import AuthCode
from models.user import User
from app.utils.base_utils import send_email
from fastapi import HTTPException, status
from app.crud.token_crud import create_access_token, create_refresh_token
from app.dependencies import get_db
from fastapi import Depends
import random


def generate_auth_code():
    return str(random.randint(100000, 999999))


def verify_auth_code(email: str, code: str, db: Session = Depends(get_db)):
    auth_code = db.query(AuthCode).filter(
        AuthCode.email == email, AuthCode.code == code).first()
    if auth_code and auth_code.expires_at > datetime.utcnow():
        db.delete(auth_code)
        db.commit()
        db.close()
        return True
    db.close()
    return False


def send_auth_code(user: User, db: Session):
    code = generate_auth_code()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    auth_code = AuthCode(user_id=user.id, code=code, expires_at=expires_at)
    db.add(auth_code)
    db.commit()

    send_email(user.email, code)

    return {
        "message": "Authorization code sent to your email again."
    }


def verify_auth_code_and_generate_tokens(user: User, code: str, db: Session):
    auth_code = db.query(AuthCode).filter(
        AuthCode.user_id == user.id,
        AuthCode.code == code,
        AuthCode.expires_at > datetime.datetime.utcnow()
    ).first()

    if not auth_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auth code not found or expired"
        )

    db.delete(auth_code)
    db.commit()

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(user_id=user.id, db=db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "registered_at": user.register_at.isoformat(),
        },
        "message": "User successfully authorized."
    }


