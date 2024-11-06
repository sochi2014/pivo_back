import smtplib
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.user import User
from app.crud.token_crud import decode_access_token
from app.dependencies import get_db
from app.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email: str, code: str):
    from_email = settings.EMAIL_SMTP
    from_password = settings.PASSWORD_SMTP

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Verification Code"

    body = f"Ваш код подтверждения: {code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.mailersend.net', 587)
        server.starttls()
        server.login(from_email, from_password)

        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_current_user(token: str, db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    print(user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    print(user)
    return user
