import uuid
import jwt
import datetime
from sqlalchemy.orm import Session
from models.refresh_token import RefreshToken
from app.config import settings
from fastapi import HTTPException, status


def create_refresh_token(user_id: int, db: Session):
    token = str(uuid.uuid4())
    expires_at = datetime.datetime.utcnow(
    ) + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(
        user_id=user_id, token=token, expires_at=expires_at)
    db.add(refresh_token)
    db.commit()
    return token


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, db: Session):
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.expires_at > datetime.datetime.utcnow()
    ).first()

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    return refresh_token


def revoke_refresh_token(token: str, db: Session):
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )

    db.delete(refresh_token)
    db.commit()

    return {"message": "Refresh token revoked successfully"}


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        print(payload)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user ID not found",
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
