from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.schemas.user_schemas import AuthCodeSchema, RegistrationSchema
from app.dependencies import get_db
from models.auth_code import AuthCode
from models.user import User
from fastapi.responses import JSONResponse
from app.utils.base_utils import send_email, get_user_by_email
from app.utils.auth_utils import (verify_auth_code_and_generate_tokens,
                                  send_auth_code, generate_auth_code)
from app.crud.token_crud import revoke_refresh_token, verify_refresh_token
from pydantic import ValidationError
import datetime
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: RegistrationSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(data.email, db)
    if user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="User with this email already exists."
        )
    new_user = User(
        email=data.email,
        username=data.username,
        register_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    code = generate_auth_code()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    auth_code = AuthCode(
        code=code,
        expires_at=expires_at,
        user_id=new_user.id
    )
    db.add(auth_code)
    db.commit()

    send_email(data.email, code)

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
