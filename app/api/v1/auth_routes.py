from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth_scheme import AuthCodeSchema, RegistrationSchema
from app.dependencies import get_db
from models.auth_code import AuthCode
from models.user import User
from fastapi.responses import JSONResponse
from app.utils.base_utils import send_email
from app.utils.auth_utils import (verify_auth_code_and_generate_tokens,
                                  send_auth_code, generate_auth_code)
from app.crud.token_crud import revoke_refresh_token, verify_refresh_token, create_access_token
from app.crud.user_crud import get_user_by_email
import datetime
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: RegistrationSchema, db: Session = Depends(get_db)):
    if not data.email or not data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both email and username are required."
        )
    user = get_user_by_email(data.email, db)
    if user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="User with this email already exists."
        )
    new_user = User(
        email=data.email,
        username=data.username,
        phone_number=data.phone_number if data.phone_number else None,
        level_id=1,
        register_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_auth_code(new_user, db)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Code has been sent to your email. Please check your inbox and use the code to complete your registration."
        }
    )


@router.post("/authorize", status_code=status.HTTP_200_OK)
async def authorize_user(auth_data: AuthCodeSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(auth_data.email, db)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found"
        )
    if not auth_data.code:
        return send_auth_code(user, db)
    return verify_auth_code_and_generate_tokens(user, auth_data.code, db)


@router.post("/verify-refresh-token", status_code=status.HTTP_200_OK)
async def verify_token_endpoint(token: str, db: Session = Depends(get_db)):
    refresh_token = verify_refresh_token(token, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Refresh token is valid",
                 "user_id": refresh_token.user_id}
    )


@router.post("/revoke-refresh-token", status_code=status.HTTP_200_OK)
async def revoke_token_endpoint(token: str, db: Session = Depends(get_db)):
    result = revoke_refresh_token(token, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result
    )


@router.post("/refresh_access_token", status_code=status.HTTP_200_OK)
async def refresh_access_endpoint(refresh_token: str, db: Session = Depends(get_db)):
    verified_token = verify_refresh_token(refresh_token, db)
    new_access_token = create_access_token(
        data={"sub": verified_token.user_id})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": new_access_token}
    )
