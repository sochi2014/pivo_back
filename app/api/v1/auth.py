from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schemas import AuthCodeSchema, RegistrationSchema
from app.crud.auth_crud import get_user_by_email, create_user
from app.crud.code_generation import verify_auth_code, generate_auth_code
from models.user import User
from models.auth_code import AuthCode
from app.database import SessionLocal
from fastapi.responses import JSONResponse
from app.utils import send_email
import datetime
import pathlib

_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: RegistrationSchema):
    user = get_user_by_email(data.email)
    if not user:
        user = create_user(
            email=data.email,
            username=data.username,
            avatar_url=data.avatar_url
        )

    code = generate_auth_code()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    auth_code = AuthCode(user_id=user.id, code=code, expires_at=expires_at)
    db: Session = SessionLocal()
    db.add(auth_code)
    db.commit()

    send_email(data.email, code)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Code was send email."}
    )


@router.post("/authorize", status_code=status.HTTP_200_OK)
async def authorize_user(auth_data: AuthCodeSchema):
    if not verify_auth_code(auth_data.email, auth_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired code."
        )

    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == auth_data.email).first()
    db.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": user.id_user,
            "email": user.email,
            "username": user.username,
            "registered_at": user.register_at.isoformat(),
            "message": "User authorized successfully."
        }
    )
