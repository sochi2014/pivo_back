from datetime import datetime, timedelta
from models.auth_code import AuthCode
from app.database import SessionLocal
import random


def generate_auth_code():
    return str(random.randint(100000, 999999))


def verify_auth_code(email: str, code: str):
    db = SessionLocal()
    auth_code = db.query(AuthCode).filter(
        AuthCode.email == email, AuthCode.code == code).first()
    if auth_code and auth_code.expires_at > datetime.utcnow():
        db.delete(auth_code)
        db.commit()
        db.close()
        return True
    db.close()
    return False
